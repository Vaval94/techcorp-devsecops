# Démonstration A4 — pipeline bloqué par un secret fictif

Le marqueur est **fictif** (aucun service réel). Il est construit à l'exécution pour ne jamais
apparaître en clair dans ce dépôt.

```powershell
git checkout -b test/secret-gate
# Faux token GitHub : préfixe ghp_ + 36 caractères aléatoires (une valeur répétitive ne serait pas détectée)
$chars = [char[]]((48..57) + (65..90) + (97..122))
$fake = "ghp_" + (-join ($chars | Get-Random -Count 36))
Set-Content -Path config-test.env -Value "GITHUB_TOKEN_FAKE=$fake"
git add config-test.env
git commit -m "test: marqueur de secret fictif (doit être bloqué)"
git push -u origin test/secret-gate
```

Résultat attendu : job **Secrets (Gitleaks)** ❌ (règle `github-pat`, valeur masquée `REDACTED`). 📸 Capture avec l'heure.

Retrait du marqueur :

```powershell
git rm config-test.env
git commit -m "fix: retrait du marqueur de secret fictif"
git push
```

Résultat attendu : les 4 jobs ✅. 📸 Capture avec l'heure.

> Le marqueur reste dans l'historique Git de la branche de test. Le scan porte sur le code livré
> (`--no-git`) ; un **vrai** secret aurait dû être **révoqué** immédiatement, l'effacer ne suffit pas.
> Supprimer ensuite la branche : `git push origin --delete test/secret-gate`.
