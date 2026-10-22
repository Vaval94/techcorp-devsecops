# Registre des risques — Orders API (Mission A1)

Échelles : **Gravité** 1 (faible) à 4 (critique) · **Probabilité** 1 (rare) à 4 (quasi certaine) · **Score** = G × P.

| ID | Risque (constat) | Gravité | Probabilité | Score | Mesure corrective | Statut |
|---|---|---|---|---|---|---|
| R1 | **Dépendances vulnérables** : `fastapi==0.115.12` tirait `starlette 0.46.2`, concernée par plusieurs CVE corrigées (ex. CVE-2025-54121, CVE-2025-62727). `requirements.txt` ne figeait pas cette dépendance transitive. | 3 | 4 | **12** | Mise à jour `fastapi 0.142.4`, `starlette 1.7.0` épinglée ; scan Trivy fs + image bloquant en CI. | Corrigé |
| R2 | **Fuite de secret dans le code** : aucun contrôle n'empêchait de pousser un token ou une clé (constat de l'ordre de mission). | 4 | 3 | **12** | Gitleaks bloquant sur chaque push/PR, `--redact` ; `.gitignore` (`.env`, `*.key`, `*.pem`) ; rotation immédiate de tout secret exposé (le retirer du code ne suffit pas, il reste dans l'historique). | Corrigé |
| R3 | **Image de base mutable et paquets superflus** : `python:3.11-slim` (tag mouvant), correctifs OS non appliqués, `setuptools`/`wheel` présents alors qu'inutiles à l'exécution. | 3 | 3 | **9** | `apt-get upgrade`, `pip` à jour, désinstallation de `setuptools`/`wheel`, scan Trivy image bloquant ; à terme figer l'image par digest `@sha256`. | Partiellement corrigé |
| R4 | **Workflow CI trop permissif / chaîne d'approvisionnement** : pas de permissions explicites, actions tierces non contrôlées. | 3 | 2 | **6** | `permissions: contents: read` global, `persist-credentials: false`, scanners lancés via images officielles à version figée (pas d'action tierce) ; à terme figer les actions `actions/*` par SHA. | Corrigé |
| R5 | **Supervision exposée sans authentification** : Grafana en accès anonyme, mot de passe admin par défaut, `/metrics` public. | 2 | 3 | **6** | Ports liés à `127.0.0.1` (laboratoire) ; en production : SSO, mot de passe admin en secret, `/metrics` réservé au réseau interne. | Accepté (laboratoire uniquement) |
| R6 | **Remédiation autonome par l'IA** : un LLM pourrait proposer et exécuter une action destructive (redémarrage, base de données). | 4 | 2 | **8** | Le LLM n'a aucun outil ni socket Docker ; sortie validée ; toute remédiation reste « en attente d'approbation » (`aiops/approve.py`). | Corrigé |
| R7 | **Injection de prompt via les logs** : un log malveillant pourrait contenir des instructions. | 3 | 2 | **6** | Logs isolés entre délimiteurs et déclarés « données non fiables », filtrés, masqués et bornés (`aiops/evidence.py`). | Corrigé |

Points forts déjà présents dans le squelette : utilisateur non root (`appuser`), `read_only`, `no-new-privileges`, ports liés à `127.0.0.1`.
