"""Détecteur AIOps TECHCORP : détection explicable + collecte de preuves + rapport.

Usage :
    python -m aiops.detector                 # analyse avec Ollama (bascule en simulé si absent)
    python -m aiops.detector --simulate-llm  # mode simulé documenté, sans LLM

Calcul de la détection (expliqué dans le verdict) :
  1. seuil absolu   : nombre de HTTP 500 sur la dernière minute >= seuil (3) — règle du sujet ;
  2. taux d'erreur  : 500 / total sur /orders >= 5 %, si le volume est suffisant (>= 5 requêtes) ;
  3. écart statistique (z-score) : (erreurs actuelles - moyenne de la baseline) / écart-type,
     la baseline étant la série glissante des minutes précédentes.
  Anomalie = seuil absolu ET (taux d'erreur OU z-score). Le seuil seul ne suffit pas :
  3 erreurs sur 10 000 requêtes, ou un niveau d'erreurs habituel, ne sont pas une anomalie.
"""
import argparse
import json
import math
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from aiops import evidence as ev
from aiops import llm
from aiops.report import render_markdown

PROMETHEUS_BASE = "http://localhost:9090"
PROMETHEUS = PROMETHEUS_BASE + "/api/v1/query"
QUERY = 'sum(increase(techcorp_http_requests_total{status="500"}[1m]))'
QUERY_TOTAL = 'sum(increase(techcorp_http_requests_total{path="/orders"}[1m]))'
QUERY_UP = 'up{job="techcorp-api"}'
QUERY_P95 = 'histogram_quantile(0.95, sum by (le) (rate(techcorp_request_duration_seconds_bucket{path="/orders"}[5m])))'


# ---------------------------------------------------------------- Prometheus (lecture seule)
def _prom(path, params, timeout=5):
    with urllib.request.urlopen(f"{PROMETHEUS_BASE}{path}?{urlencode(params)}", timeout=timeout) as response:
        payload = json.load(response)
    return payload.get("data", {}).get("result", [])


def instant(query):
    series = _prom("/api/v1/query", {"query": query})
    if not series:
        return 0.0
    value = float(series[0]["value"][1])
    return 0.0 if math.isnan(value) else value


def get_error_count():
    return instant(QUERY)


def history(query, minutes=15, step="60s"):
    """Série des valeurs sur la fenêtre [maintenant - minutes ; maintenant]."""
    end = time.time()
    series = _prom("/api/v1/query_range", {"query": query, "start": end - minutes * 60, "end": end, "step": step})
    if not series:
        return []
    return [0.0 if math.isnan(float(v)) else float(v) for _, v in series[0]["values"]]


# ---------------------------------------------------------------- Détection
def detect_anomaly(count, threshold=3):
    """Règle de seuil fixe du sujet (conservée pour comparaison et compatibilité)."""
    return count >= threshold


def evaluate(errors_now, total_now, baseline, threshold=3, rate_threshold=0.05,
             min_requests=5, z_threshold=3.0, min_baseline_points=5, window="1m"):
    """Renvoie un verdict explicable. `baseline` = erreurs/min des minutes précédentes."""
    raisons = []
    error_rate = errors_now / total_now if total_now > 0 else 0.0

    threshold_hit = errors_now >= threshold
    raisons.append(f"Seuil absolu : {errors_now:g} HTTP 500 sur {window} "
                   f"({'≥' if threshold_hit else '<'} {threshold}).")

    rate_hit = total_now >= min_requests and error_rate >= rate_threshold
    if total_now < min_requests:
        raisons.append(f"Taux d'erreur non significatif : seulement {total_now:g} requêtes (< {min_requests}).")
    else:
        raisons.append(f"Taux d'erreur : {error_rate:.0%} ({'≥' if rate_hit else '<'} {rate_threshold:.0%}).")

    z_score, z_hit = None, False
    mean = stdev = None
    if len(baseline) >= min_baseline_points:
        mean = statistics.fmean(baseline)
        stdev = statistics.pstdev(baseline)
        if stdev > 0:
            z_score = (errors_now - mean) / stdev
            z_hit = z_score >= z_threshold
            raisons.append(f"Écart à la baseline : z = {z_score:.1f} (moyenne {mean:.1f}, écart-type {stdev:.1f}, "
                           f"{'≥' if z_hit else '<'} {z_threshold}).")
        else:
            # Baseline parfaitement stable : tout dépassement net du niveau habituel est inhabituel.
            z_hit = errors_now > mean
            raisons.append(f"Baseline stable à {mean:.1f} erreur/min : niveau actuel "
                           f"{'au-dessus' if z_hit else 'identique ou inférieur'}.")
    else:
        raisons.append(f"Baseline insuffisante ({len(baseline)} points < {min_baseline_points}) : z-score non calculé.")

    anomaly = threshold_hit and (rate_hit or z_hit)
    severity = "aucune"
    if anomaly:
        severity = "critique" if error_rate >= 0.5 else "avertissement"
    return {
        "anomalie": anomaly,
        "severite": severity,
        "fenetre": window,
        "errors_now": errors_now,
        "requests_now": total_now,
        "error_rate_pct": round(error_rate * 100, 1),
        "baseline": {"points": len(baseline), "moyenne": None if mean is None else round(mean, 2),
                     "ecart_type": None if stdev is None else round(stdev, 2)},
        "z_score": None if z_score is None else round(z_score, 2),
        "regles": {"seuil_absolu": threshold_hit, "taux_erreur": rate_hit, "z_score": z_hit},
        "raisons": raisons,
        "verdict": ("ANOMALIE : " if anomaly else "Pas d'anomalie : ")
                   + ("seuil dépassé et confirmé par le taux d'erreur ou l'écart à la baseline."
                      if anomaly else "les règles combinées ne sont pas toutes réunies."),
    }


# ---------------------------------------------------------------- Rapport
def make_report(count, logs, hypothesis, detection=None, analysis=None, context=None):
    return {
        "incident_id": "INC-2026-1042",
        "genere_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "observations": {"http_500_last_minute": count, "logs": logs, **(context or {})},
        "detection": detection or {},
        "hypothesis": hypothesis,
        "analyse_ia": analysis or {},
        "checks_read_only": (analysis or {}).get("controles_non_destructifs", []),
        "confidence": "unverified",
        "human_approval_required": True,
        "approbations": [],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Détecteur AIOps TECHCORP")
    parser.add_argument("--simulate-llm", action="store_true", help="ne pas appeler Ollama (mode simulé documenté)")
    parser.add_argument("--model", default=llm.OLLAMA_MODEL)
    parser.add_argument("--window-minutes", type=int, default=15, help="taille de la baseline glissante")
    parser.add_argument("--logs-since", default="15m")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # console Windows

    try:
        errors_now = instant(QUERY)
        total_now = instant(QUERY_TOTAL)
        up = instant(QUERY_UP)
        p95 = instant(QUERY_P95)
        series = history(QUERY + " or vector(0)", minutes=args.window_minutes)
    except OSError as exc:
        print(f"Prometheus injoignable ({exc}). Aucune donnée inventée : arrêt.")
        return 2
    baseline = series[:-1]  # la dernière minute est la mesure courante, pas la baseline
    detection = evaluate(errors_now, total_now, baseline)

    raw_logs, logs_source = ev.collect_docker_logs(since=args.logs_since)
    scenario = ev.read_file_lines("docs/fake_incident.log")
    logs, log_stats = ev.bound_logs(scenario + raw_logs)
    change = ev.load_change()
    correlation = ev.correlate(change, ev.first_error_time(scenario + raw_logs))

    evidence = {
        "detection": detection,
        "metriques": {"up": up, "latence_p95_s": round(p95, 4), "http_500_serie_par_minute": series},
        "changement": change,
        "correlation": correlation,
        "logs": logs,
    }
    analysis, mode, note = llm.analyze(evidence, simulate=args.simulate_llm, model=args.model)
    hypothesis = analysis["hypotheses"][0]["hypothese"] if analysis["hypotheses"] else "aucune hypothèse produite"

    report = make_report(errors_now, logs, hypothesis, detection, analysis, context={
        "requests_last_minute": total_now, "up": up, "latence_p95_s": round(p95, 4),
        "serie_http_500_par_minute": series, "source_logs": logs_source, "volume_logs": log_stats,
        "changement": change, "correlation": correlation,
    })
    report["analyse_ia_mode"] = mode
    report["analyse_ia_note"] = note

    Path("report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    Path("incident-report.md").write_text(render_markdown(report), encoding="utf-8")
    print(detection["verdict"])
    for r in detection["raisons"]:
        print(" -", r)
    print(f"anomaly= {detection['anomalie']}  | analyse IA : {mode} | report.json + incident-report.md générés")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
