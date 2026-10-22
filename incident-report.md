# Rapport d'incident INC-2026-1042

*Généré le 2026-10-22T21:00:22+00:00 — statut : **hypothèses non validées**, aucune action exécutée automatiquement.*

## 1. Résumé
- Verdict de détection : **ANOMALIE : seuil dépassé et confirmé par le taux d'erreur ou l'écart à la baseline.**
- Sévérité : critique
- HTTP 500 sur 1 min : 50.18638058005273 / 50.18638058005273 requêtes (100.0 %)
- Cible Prometheus `up` : 1.0 — latence p95 : 0.0047 s

## 2. Contexte du changement
- Changement : CHG-2026-0247 — version 2.4.7 déployée le 2026-10-22T10:15:00Z
- Corrélation : Première erreur 2.0 min après le déploiement 2.4.7. Proximité temporelle = indice, PAS une preuve de causalité : d'autres changements ou une cause externe (base de données, réseau) restent possibles.

## 3. Calcul de la détection
- Seuil absolu : 50.1864 HTTP 500 sur 1m (≥ 3).
- Taux d'erreur : 100% (≥ 5%).
- Écart à la baseline : z = 0.0 (moyenne 49.2, écart-type 52.1, < 3.0).

## 4. Preuves collectées
- Source des logs : `docker compose logs --since 15m --tail 500 api`
- Volume : 504 lignes lues, 463 pertinentes, 40 conservées
- Extraits (masqués, bornés, traités comme données non fiables) :

```text
api-1  | 2026-10-22T21:00:11.888086810Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:11.888931720Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:12.400019144Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:12.400786050Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:12.910360725Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:12.910941030Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:13.423388447Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:13.423782540Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:13.931828250Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:13.932496739Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:14.454474311Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:14.455533257Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:14.975808025Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:14.976343500Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:15.489717410Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:15.490350348Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:16.001714081Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:16.002223716Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:16.513011304Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:16.514276219Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:17.022294912Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:17.023423461Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:17.534000584Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:17.534428695Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:18.048772933Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:18.049319268Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:18.563150983Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:18.563795033Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:19.074496640Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:19.075153655Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:19.586309054Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:19.587178833Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:20.101520877Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:20.102153013Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:20.612719003Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:20.613293844Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:21.125199153Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:21.125771781Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T21:00:21.637668508Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T21:00:21.638289802Z INFO:     172.22.0.1:47446 - "GET /orders HTTP/1.1" 500 Internal Server Error
```

## 5. Analyse IA (simulé)
*mode simulé demandé (--simulate-llm)*

### Symptômes
- 50.18638058005273 HTTP 500 sur /orders sur 1 min
- taux d'erreur 100.0 %

### Hypothèses (aucune n'est validée)
**H1. La base de données (ou le pool de connexions) ne répond pas dans les délais.** — confiance : *moyenne*
- Preuves : logs : db_connection_timeout sur /orders
- Preuves manquantes : métriques côté base (connexions, latence, CPU), état du pool de connexions

**H2. La version 2.4.7 a introduit une régression (configuration ou code d'accès à la base).** — confiance : *faible*
- Preuves : corrélation temporelle : 2.0 min après le déploiement
- Preuves manquantes : diff 2.4.6 → 2.4.7, reproduction sur 2.4.6, erreurs absentes avant 10:15

### Contrôles non destructifs proposés
- Consulter /health et la cible Prometheus (up)
- Lire les métriques de connexions de la base (lecture seule)
- Comparer la configuration 2.4.6 et 2.4.7 (diff, sans modification)
- Vérifier si d'autres services utilisant la même base sont dégradés

### Limites de l'analyse
- Analyse simulée (Ollama indisponible) : règles déterministes, pas de raisonnement LLM
- Aucune métrique côté base de données collectée
- Environnement de laboratoire : panne injectée par SIMULATE_FAILURE

## 6. Remédiation proposée — EN ATTENTE D'APPROBATION
| # | Action | Risque | Statut |
|---|---|---|---|
| 1 | Rollback vers la version 2.4.6 | moyen : perte des correctifs de 2.4.7 | approuvé (à exécuter manuellement) |
| 2 | Redémarrage du service api | faible à moyen : interruption brève, peut masquer la cause | en attente d'approbation |

## 7. Décisions humaines
- 2026-10-22T21:05:53+00:00 — **approuvé** de l'action 1 « Rollback vers la version 2.4.6 » par Valentin : rollback validé après vérification du diff

## 8. Règles de sécurité appliquées
- Logs traités comme données non fiables, jamais exécutés.
- Secrets et identifiants masqués avant envoi au LLM ; volume de logs borné.
- Le LLM n'a accès à aucun outil ni au socket Docker.
- Aucune action sur la production ni sur la base de données sans approbation SRE.
