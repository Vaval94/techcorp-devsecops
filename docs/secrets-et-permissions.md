# Secrets et permissions (Mission A5)

## Secrets GitHub Actions
- Stockés chiffrés par GitHub (*Settings → Secrets and variables → Actions*), injectés à l'exécution via `${{ secrets.NOM }}`.
- Masqués automatiquement dans les logs (`***`), mais un script peut encore les exfiltrer : ne jamais les afficher ni les écrire dans un artefact.
- Non transmis aux workflows déclenchés par une PR venant d'un **fork**.
- **Secrets d'environnement** (ex. `production`) : protégés par des relecteurs obligatoires avant usage.
- Préférer **OIDC** (jeton éphémère échangé auprès du cloud) aux clés longue durée.

## Permissions minimales du GITHUB_TOKEN
- Jeton créé pour chaque exécution, valable le temps du job.
- Par défaut, il peut avoir des droits d'écriture : on le restreint explicitement.
- Ici : `permissions: contents: read` au niveau du workflow. Si un job doit publier un résultat (ex. `security-events: write` pour SARIF), on l'accorde **à ce job uniquement**.
- `persist-credentials: false` évite que le jeton reste dans `.git/config` pour les étapes suivantes.

## Pourquoi un Kubernetes Secret non chiffré n'est pas un coffre-fort
- Les valeurs sont seulement **encodées en base64** : `base64 -d` suffit à les lire.
- Stockées dans **etcd en clair** si le chiffrement au repos (`EncryptionConfiguration` / KMS) n'est pas activé : un accès à etcd ou à ses sauvegardes expose tout.
- Toute personne ayant le droit RBAC `get secrets` dans le namespace, ou pouvant créer un pod qui le monte, peut les lire.
- Pas de rotation automatique, peu d'audit d'accès, et un Secret commité dans Git (YAML) y reste à vie.
- Un vrai coffre-fort (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault…) apporte : chiffrement géré, contrôle d'accès fin, audit, rotation, secrets dynamiques. Côté Kubernetes : External Secrets Operator, Sealed Secrets ou CSI Secrets Store.
