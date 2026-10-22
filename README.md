# TECHCORP — TP intégrateur DevSecOps & AIOps

Mission SRE sur l'**Orders API** : sécuriser la livraison (Mission A), détecter et qualifier
l'incident **INC-2026-1042** (Mission B), produire une analyse IA prudente et un rapport
validé par un humain (Mission C).

## Contenu du dépôt

| Élément | Rôle |
|---|---|
| `app/` | API FastAPI (`/orders`, `/health`, `/metrics`), dépendances figées et corrigées |
| `Dockerfile` | Image non root, correctifs OS, `setuptools`/`wheel` retirés, healthcheck |
| `docker-compose.yml` | API + Prometheus + Grafana (liés à `127.0.0.1`), panne pilotée par `SIMULATE_FAILURE` |
| `.github/workflows/ci.yml` | Tests, **Gitleaks**, **Trivy** dépendances + image — quality gate |
| `.trivyignore` | Exceptions approuvées (vide : aucune exception) |
| `monitoring/` | Prometheus, règles d'alerte, Grafana provisionné (source + dashboard) |
| `aiops/detector.py` | Détection explicable : seuil + taux d'erreur + z-score sur baseline glissante |
| `aiops/evidence.py` | Logs bornés et masqués, contexte du changement, corrélation (≠ causalité) |
| `aiops/llm.py` | Appel Ollama `POST /api/generate` (JSON structuré), mode simulé, validation |
| `aiops/approve.py` | Enregistrement d'une décision humaine — n'exécute rien |
| `tests/` | Tests du détecteur, des preuves, du LLM et de l'API |
| `docs/` | Registre des risques, quality gate, A5, démo A4, PromQL, plan de restauration, soutenance |

## Prérequis
Docker Desktop, Git, Python 3.11+, VS Code. Ollama facultatif (`ollama pull llama3.2`).

## 1. Démarrer le laboratoire (PowerShell)
```powershell
docker compose up --build -d
docker compose ps
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/orders
python -m pip install -r requirements-dev.txt
python -m pytest -q
```
- Prometheus : http://localhost:9090 (Status → Target health : `techcorp-api` UP)
- Grafana : http://localhost:3000 (admin / admin) → Dashboards → TECHCORP → **TECHCORP — Orders API (SRE)**

## 2. Déclencher l'incident (local uniquement)
```powershell
$env:SIMULATE_FAILURE = "true"
docker compose up -d --force-recreate api
1..10 | ForEach-Object { try { Invoke-WebRequest http://localhost:8000/orders -UseBasicParsing | Out-Null } catch { Write-Host "HTTP 500 simulé" } }
```
Attendre 30 à 60 s (collecte Prometheus toutes les 5 s, `increase[1m]`), puis vérifier l'alerte
`ElevatedHTTP500` dans Prometheus → Alerts.

## 3. Détection et rapport
```powershell
python -m aiops.detector                 # avec Ollama si disponible, sinon bascule en mode simulé
python -m aiops.detector --simulate-llm  # mode simulé explicite
```
Produit `report.json` et `incident-report.md`. Enregistrer la décision humaine :
```powershell
python -m aiops.approve --action 1 --decision approuvé --by "Prénom Nom" --comment "rollback validé après diff"
```

## 4. Fin d'incident et nettoyage
```powershell
$env:SIMULATE_FAILURE = "false"
docker compose up -d --force-recreate api
docker compose down
```

## Règles de sécurité
Aucun secret réel (le marqueur de la démo A4 est fictif et généré à la volée). Logs traités comme
données non fiables. Le LLM n'a ni outil ni accès au socket Docker. Aucune remédiation sans
approbation humaine. Aucune action sur une base de données ou sur la production.
