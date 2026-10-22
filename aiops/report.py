"""Rendu Markdown du rapport d'incident à partir de report.json."""


def _bullets(items):
    return "\n".join(f"- {i}" for i in items) if items else "- (aucun)"


def render_markdown(r: dict) -> str:
    obs, det, ia = r.get("observations", {}), r.get("detection", {}), r.get("analyse_ia", {})
    corr = obs.get("correlation") or {}
    change = obs.get("changement") or {}
    lines = [
        f"# Rapport d'incident {r.get('incident_id')}",
        "",
        f"*Généré le {r.get('genere_le')} — statut : **hypothèses non validées**, "
        "aucune action exécutée automatiquement.*",
        "",
        "## 1. Résumé",
        f"- Verdict de détection : **{det.get('verdict', 'n/a')}**",
        f"- Sévérité : {det.get('severite', 'n/a')}",
        f"- HTTP 500 sur 1 min : {obs.get('http_500_last_minute')} / {obs.get('requests_last_minute')} requêtes "
        f"({det.get('error_rate_pct')} %)",
        f"- Cible Prometheus `up` : {obs.get('up')} — latence p95 : {obs.get('latence_p95_s')} s",
        "",
        "## 2. Contexte du changement",
        f"- Changement : {change.get('change_id', 'n/a')} — version {change.get('version', 'n/a')} "
        f"déployée le {change.get('deployed_at', 'n/a')}",
        f"- Corrélation : {corr.get('lecture', 'n/a')}",
        "",
        "## 3. Calcul de la détection",
        _bullets(det.get("raisons", [])),
        "",
        "## 4. Preuves collectées",
        f"- Source des logs : `{obs.get('source_logs')}`",
        "- Volume : {lignes_lues} lignes lues, {lignes_pertinentes} pertinentes, {lignes_conservées} conservées".format(
            **(obs.get("volume_logs") or {"lignes_lues": 0, "lignes_pertinentes": 0, "lignes_conservées": 0})),
        "- Extraits (masqués, bornés, traités comme données non fiables) :",
        "",
        "```text",
        *(obs.get("logs") or ["(aucun log)"]),
        "```",
        "",
        f"## 5. Analyse IA ({r.get('analyse_ia_mode', 'n/a')})",
        f"*{r.get('analyse_ia_note', '')}*",
        "",
        "### Symptômes",
        _bullets(ia.get("symptomes", [])),
        "",
        "### Hypothèses (aucune n'est validée)",
    ]
    for i, h in enumerate(ia.get("hypotheses", []), 1):
        lines += [f"**H{i}. {h['hypothese']}** — confiance : *{h['confiance']}*",
                  f"- Preuves : {', '.join(h['preuves']) or 'aucune'}",
                  f"- Preuves manquantes : {', '.join(h['preuves_manquantes']) or 'non précisées'}", ""]
    lines += [
        "### Contrôles non destructifs proposés",
        _bullets(ia.get("controles_non_destructifs", [])),
        "",
        "### Limites de l'analyse",
        _bullets(ia.get("limites", [])),
        "",
        "## 6. Remédiation proposée — EN ATTENTE D'APPROBATION",
        "| # | Action | Risque | Statut |",
        "|---|---|---|---|",
    ]
    for i, a in enumerate(ia.get("remediation_proposee", []), 1):
        lines.append(f"| {i} | {a['action']} | {a['risque']} | {a['statut']} |")
    lines += ["", "## 7. Décisions humaines"]
    if r.get("approbations"):
        for a in r["approbations"]:
            lines.append(f"- {a['date']} — **{a['decision']}** de l'action {a['action_index']} "
                         f"« {a['action']} » par {a['par']} : {a.get('commentaire', '')}")
    else:
        lines.append("- Aucune décision enregistrée. Aucune action n'est autorisée.")
    lines += ["", "## 8. Règles de sécurité appliquées",
              "- Logs traités comme données non fiables, jamais exécutés.",
              "- Secrets et identifiants masqués avant envoi au LLM ; volume de logs borné.",
              "- Le LLM n'a accès à aucun outil ni au socket Docker.",
              "- Aucune action sur la production ni sur la base de données sans approbation SRE.", ""]
    return "\n".join(lines)
