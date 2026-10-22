# Quality gate — politique de blocage des PR (Mission A3)

Le pipeline `.github/workflows/ci.yml` comporte 4 contrôles. **Une PR ne peut être fusionnée que si les 4 sont verts** (à activer dans GitHub : *Settings → Branches → Branch protection rule* sur `main`, « Require status checks to pass »).

## Ce qui bloque automatiquement

| Contrôle | Bloque si… | Pourquoi |
|---|---|---|
| Tests Pytest | un test échoue | régression fonctionnelle |
| Gitleaks | **un secret est détecté**, quelle que soit sa nature | un secret poussé est compromis : aucune tolérance |
| Trivy fs (dépendances) | vulnérabilité **CRITICAL ou HIGH avec correctif disponible** | exploitable et corrigeable : aucune raison de livrer |
| Trivy image | vulnérabilité **CRITICAL ou HIGH avec correctif disponible** (OS + Python) | idem, sur ce qui tourne réellement |

## Ce qui ne bloque pas (mais est tracé)

- **MEDIUM / LOW** : rapport complet en artefact CI, traitement planifié.
- **HIGH sans correctif** (`--ignore-unfixed`) : rien à mettre à jour ; suivi dans le registre des risques avec mesure compensatoire.
- **Mauvaises configurations** (`trivy config`) : informatif, revue humaine.

## Distinguer les résultats

- **Vulnérabilité exploitable** : composant présent dans l'image, code vulnérable atteignable (route exposée, entrée utilisateur), correctif disponible. → corriger avant fusion.
- **Faux positif** : la détection ne correspond pas à un risque réel (version mal identifiée, fonction vulnérable non utilisée, secret factice de test). → démontrer pourquoi (preuve écrite), puis exception.
- **Exception approuvée** : risque réel mais accepté temporairement (pas de correctif, mesure compensatoire en place). → exception formelle.

## Procédure d'exception

Une exception n'est valable que si elle figure dans `.trivyignore` (ou `.gitleaksignore`) **avec un commentaire** indiquant :
justification, propriétaire, date d'approbation, **date d'expiration** (30 jours max), approbateur sécurité.
L'ajout passe par une PR relue par un responsable sécurité. Les exceptions expirées sont supprimées.
**Aucune exception n'est possible pour un vrai secret** : on le révoque et on le remplace.
