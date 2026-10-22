# Requêtes PromQL utilisées (Mission B)

| Objectif | Requête |
|---|---|
| Disponibilité de la cible | `up{job="techcorp-api"}` |
| Requêtes 200 / 500 (débit) | `sum by (status) (rate(techcorp_http_requests_total[1m]))` |
| HTTP 500 sur la dernière minute | `sum(increase(techcorp_http_requests_total{status="500"}[1m]))` |
| Taux d'erreur /orders (%) | `100 * sum(rate(techcorp_http_requests_total{path="/orders",status="500"}[1m])) / sum(rate(techcorp_http_requests_total{path="/orders"}[1m]))` |
| Latence p95 /orders | `histogram_quantile(0.95, sum by (le) (rate(techcorp_request_duration_seconds_bucket{path="/orders"}[5m])))` |
| Version déployée | `techcorp_build_info` |

## Seuil d'alerte vs détection d'anomalie (B4)

`ElevatedHTTP500` déclenche dès **3 erreurs en 1 minute** pendant 15 s. C'est un **seuil fixe** :
- il ignore le volume : 3 erreurs sur 5 requêtes (60 %) et 3 sur 10 000 (0,03 %) donnent la même alerte ;
- il ignore le comportement habituel : un service qui a « normalement » 3 erreurs/min alerte en permanence ;
- il ne voit pas une hausse anormale sous le seuil.

Une **détection statistique** compare la valeur actuelle à une **référence apprise** (baseline glissante) :
moyenne et écart-type des minutes précédentes, puis **z-score** = (valeur − moyenne) / écart-type.
Une anomalie est un écart improbable par rapport à cette référence (ex. z ≥ 3), indépendamment d'une valeur absolue.
`aiops/detector.py` combine les deux : seuil absolu **et** (taux d'erreur ≥ 5 % **ou** z-score ≥ 3).
