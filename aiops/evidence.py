"""Collecte de preuves : logs bornés et masqués, contexte du changement, corrélation.

Règles appliquées (sujet, section 9) :
- les logs sont des DONNÉES non fiables : ils ne sont jamais exécutés ni interprétés
  comme des instructions ;
- seules les lignes utiles sont conservées, en nombre et en taille bornés ;
- les secrets et identifiants sont masqués avant tout envoi au LLM ;
- la collecte est en lecture seule (docker compose logs) et n'est pas confiée au LLM.
"""
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# (motif, remplacement) — l'ordre compte : les motifs spécifiques d'abord.
SECRET_PATTERNS = [
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "gh*_***MASQUÉ***"),
    (re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"), "AKIA***MASQUÉ***"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-~+/]+=*"), "Bearer ***MASQUÉ***"),
    (re.compile(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|authorization)\b\s*[=:]\s*\S+"), r"\1=***MASQUÉ***"),
    (re.compile(r"(?i)\b(postgres|postgresql|mysql|mongodb|redis)://[^\s:@]+:[^\s@]+@"), r"\1://***:***@"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "***EMAIL***"),
]
RELEVANT = re.compile(r"ERROR|CRITICAL|WARN|Traceback|Exception|timeout|\b5\d\d\b|deploy", re.I)
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
TIMESTAMP = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})")


def mask(line: str) -> str:
    """Masque tokens, clés, mots de passe et e-mails dans une ligne de log."""
    for pattern, replacement in SECRET_PATTERNS:
        line = pattern.sub(replacement, line)
    return line


def bound_logs(lines, max_lines=40, max_chars=300):
    """Ne garde que les lignes pertinentes, masquées, tronquées et en nombre limité."""
    relevant = [l for l in lines if RELEVANT.search(l)]
    cleaned = []
    for line in relevant[-max_lines:]:
        line = CONTROL_CHARS.sub(" ", line).strip()
        line = mask(line)
        if len(line) > max_chars:
            line = line[:max_chars] + " …[tronqué]"
        cleaned.append(line)
    stats = {"lignes_lues": len(lines), "lignes_pertinentes": len(relevant), "lignes_conservées": len(cleaned)}
    return cleaned, stats


def collect_docker_logs(service="api", since="15m", tail=500):
    """Lecture seule des logs du service via docker compose. Renvoie (lignes, note)."""
    cmd = ["docker", "compose", "logs", "--no-color", "--timestamps", "--since", since, "--tail", str(tail), service]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                             timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], f"logs indisponibles ({exc.__class__.__name__})"
    if out.returncode != 0:
        return [], "logs indisponibles (docker compose a échoué)"
    return out.stdout.splitlines(), f"docker compose logs --since {since} --tail {tail} {service}"


def read_file_lines(path):
    p = Path(path)
    return p.read_text(encoding="utf-8").splitlines() if p.exists() else []


def load_change(path="docs/change.json"):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def first_error_time(lines):
    for line in lines:
        if re.search(r"ERROR", line) and TIMESTAMP.search(line):
            return TIMESTAMP.search(line).group(1)
    return None


def correlate(change, first_error):
    """Corrélation temporelle uniquement : elle ne prouve pas la causalité."""
    if not change or not first_error:
        return {"délai_minutes": None, "lecture": "Corrélation impossible : changement ou première erreur inconnus."}
    deployed = datetime.fromisoformat(change["deployed_at"].replace("Z", "+00:00"))
    err = datetime.fromisoformat(first_error).replace(tzinfo=timezone.utc)
    if deployed.tzinfo is None:
        deployed = deployed.replace(tzinfo=timezone.utc)
    delta = round((err - deployed).total_seconds() / 60, 1)
    return {
        "délai_minutes": delta,
        "lecture": (f"Première erreur {delta} min après le déploiement {change.get('version')}. "
                    "Proximité temporelle = indice, PAS une preuve de causalité : "
                    "d'autres changements ou une cause externe (base de données, réseau) restent possibles."),
    }
