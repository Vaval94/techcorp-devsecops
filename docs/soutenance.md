# Soutenance — déroulé de la démo (5 min)

1. **Pipeline rouge puis vert** (1 min) : captures horodatées du job Gitleaks en échec (branche `test/secret-gate`), puis des 4 jobs verts.
2. **Grafana avant / pendant l'incident** (1 min) : dashboard « TECHCORP — Orders API », 0 % d'erreur puis 100 %, courbe HTTP 500 au-dessus du seuil.
3. **Détecteur** (1 min) : `python -m aiops.detector`, lire les 3 raisons du verdict (seuil, taux, z-score).
4. **Rapport IA** (1 min) : `incident-report.md`, hypothèses avec niveau de confiance, remédiation en attente.
5. **Contestation + plan** (1 min) : voir ci-dessous, puis `docs/plan-restauration.md`.

## Hypothèse contestée
**« La version 2.4.7 a causé les timeouts de base de données. »**
- Preuve disponible : uniquement une **proximité temporelle** (2 min).
- Ce qui manque : le diff de 2.4.7, l'absence d'erreurs juste avant 10:15, les métriques de la base, une reproduction avec 2.4.6.
- Explications concurrentes : saturation de la base, incident réseau, autre service ayant épuisé les connexions, pic de trafic (`request_rate_spike` dans les logs).
- En laboratoire, la panne est d'ailleurs **injectée** par `SIMULATE_FAILURE` : l'hypothèse « régression 2.4.7 » serait fausse, ce qui montre pourquoi la corrélation ne suffit pas.

## Questions probables
- *Pourquoi ne pas laisser l'IA faire le rollback ?* Conclusions non validées, action à risque, responsabilité humaine (exigence du DSI).
- *Que fait-on d'un faux positif Trivy ?* Preuve écrite, exception datée dans `.trivyignore`, revue sécurité.
- *Pourquoi un z-score ?* Il tient compte du comportement habituel, contrairement à un seuil fixe.
