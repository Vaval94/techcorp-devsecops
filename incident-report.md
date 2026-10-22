# Rapport d'incident INC-2026-1042

*Généré le 2026-10-22T23:31:42+00:00 — statut : **hypothèses non validées**, aucune action exécutée automatiquement.*

## 1. Résumé
- Verdict de détection : **ANOMALIE : seuil dépassé et confirmé par le taux d'erreur ou l'écart à la baseline.**
- Sévérité : critique
- HTTP 500 sur 1 min : 73.02036151070327 / 77.04642163185997 requêtes (94.8 %)
- Cible Prometheus `up` : 1.0 — latence p95 : 0.0047 s

## 2. Contexte du changement
- Changement : CHG-2026-0247 — version 2.4.7 déployée le 2026-10-22T10:15:00Z
- Corrélation : Première erreur 2.0 min après le déploiement 2.4.7. Proximité temporelle = indice, PAS une preuve de causalité : d'autres changements ou une cause externe (base de données, réseau) restent possibles.

## 3. Calcul de la détection
- Seuil absolu : 73.0204 HTTP 500 sur 1m (≥ 3).
- Taux d'erreur : 95% (≥ 5%).
- Baseline insuffisante (0 points < 5) : z-score non calculé.

## 4. Preuves collectées
- Source des logs : `docker compose logs --since 15m --tail 500 api`
- Volume : 205 lignes lues, 186 pertinentes, 40 conservées
- Extraits (masqués, bornés, traités comme données non fiables) :

```text
api-1  | 2026-10-22T23:29:46.230456105Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:46.230716644Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:46.743445059Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:46.744117643Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:47.256185357Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:47.256561918Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:47.765868166Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:47.766517970Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:48.280378163Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:48.280780997Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:48.793519937Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:48.794003160Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:49.306345993Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:49.307050888Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:49.816846465Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:49.817261748Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:50.322663737Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:50.322935328Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:50.827455198Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:50.827947729Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:51.333792578Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:51.334215061Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:51.842062733Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:51.842496317Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:52.349362714Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:52.349969212Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:52.856900848Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:52.857158443Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:53.369394720Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:53.370066554Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:53.878960840Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:53.879716171Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:54.391716878Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:54.392290994Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:54.903713374Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:54.904129029Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:55.412619312Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:55.413346258Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
api-1  | 2026-10-22T23:29:55.922229054Z ERROR:    order_processing_failed db_connection_timeout event=INC-2026-1042 release=2.4.7
api-1  | 2026-10-22T23:29:55.922788232Z INFO:     172.22.0.1:46916 - "GET /orders HTTP/1.1" 500 Internal Server Error
```

## 5. Analyse IA (ollama:llama3.2)
*réponse Ollama validée et normalisée*

### Symptômes
- Erreur de connexion à la base de données
- Erreur HTTP 500

### Hypothèses (aucune n'est validée)
**H1. Une erreur de connexion à la base de données a causé une erreur HTTP 500** — confiance : *faible*
- Preuves : Seuil absolu : 73.0204 HTTP 500 sur 1m (≥ 3)., Taux d'erreur : 95% (≥ 5%).
- Preuves manquantes : Corrélation temporelle entre les erreurs de connexion et les erreurs HTTP 500

### Contrôles non destructifs proposés
- Vérifier les logs pour identifier les erreurs de connexion
- Vérifier les métriques pour comprendre le taux d'erreur

### Limites de l'analyse
- Seuil absolu : 3
- Taux d'erreur : 5%

## 6. Remédiation proposée — EN ATTENTE D'APPROBATION
| # | Action | Risque | Statut |
|---|---|---|---|
| 1 | Vérifier les logs pour identifier les erreurs de connexion et les corriger | Éventuelle perte de données en cas d'erreur de connexion | approuvé (à exécuter manuellement) |

## 7. Décisions humaines
- 2026-10-22T23:37:15+00:00 — **approuvé** de l'action 1 « Vérifier les logs pour identifier les erreurs de connexion et les corriger » par Valentin : vérification des logs validée, aucune action sur la base sans DBA

## 8. Règles de sécurité appliquées
- Logs traités comme données non fiables, jamais exécutés.
- Secrets et identifiants masqués avant envoi au LLM ; volume de logs borné.
- Le LLM n'a accès à aucun outil ni au socket Docker.
- Aucune action sur la production ni sur la base de données sans approbation SRE.
