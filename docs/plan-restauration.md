# Plan de restauration — INC-2026-1042 (Mission D)

> Aucune étape n'est exécutée sans l'approbation explicite du responsable SRE d'astreinte,
> enregistrée avec `python -m aiops.approve`.

## 1. Option retenue : rollback vers 2.4.6
- **Justification** : la dégradation commence 2 min après le déploiement 2.4.7 et 2.4.6 était stable. C'est une corrélation, pas une preuve : le rollback est aussi un **test d'hypothèse**.
- **Risque** : moyen — perte des correctifs de 2.4.7 ; si une migration de schéma a accompagné 2.4.7, le rollback applicatif peut être incompatible → **vérifier d'abord l'absence de migration**. Si la cause est la base de données, le rollback ne corrigera rien.
- **Alternative** si une migration existe ou si la base est en cause : escalade DBA, aucune action sur la base sans eux.

## 2. Préconditions (contrôles non destructifs)
1. Diff 2.4.6 → 2.4.7 : configuration de connexion, timeouts, taille du pool.
2. Absence de migration de base liée à 2.4.7.
3. État de la base (connexions, latence) en lecture seule.
4. Image 2.4.6 disponible et ayant passé la CI.

## 3. Exécution (après approbation)
Déployer l'image 2.4.6 par le pipeline habituel (même chemin qu'une livraison, pas de commande manuelle en production).
En laboratoire, l'équivalent est : `$env:SIMULATE_FAILURE="false"; docker compose up -d --force-recreate api`.

## 4. Validation
- `/health` = 200 ; `up` = 1.
- Taux d'erreur /orders < 1 % pendant 15 min ; HTTP 500 retombés à la baseline.
- Latence p95 revenue au niveau habituel ; alerte `ElevatedHTTP500` résolue.
- Détecteur : `anomaly= False`.

## 5. Observabilité post-changement
Surveillance renforcée 1 h (dashboard ouvert, alertes actives), annotation Grafana « rollback 2.4.6 » avec l'heure, critère d'annulation : si le taux d'erreur remonte, arrêt et escalade.

## 6. Post-mortem (sans recherche de coupable, sous 5 jours)
Chronologie, impact (durée, requêtes en erreur), cause racine **prouvée**, ce qui a bien/mal fonctionné, actions : test de connexion à la base en pré-production, déploiement progressif (canary), alerte sur le taux d'erreur plutôt que sur un seuil fixe.
