#!/usr/bin/env bash
set -euo pipefail

# git_sync_safe.sh
# Tentative automatisée et non destructive pour synchroniser la branche courante
# avec origin/main : crée une branche de backup, stashe les changements non committés,
# fait un fetch + rebase sur origin/main, et pousse si tout est OK.

print() { printf '%s\n' "$*"; }

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  print "Erreur : ce script doit être lancé depuis la racine d'un dépôt git." >&2
  exit 2
fi

branch=$(git rev-parse --abbrev-ref HEAD)
ts=$(date +%Y%m%d%H%M%S)
backup_branch="backup/${branch}-${ts}"

print "Branche courante : ${branch}"
print "Création d'une branche de sauvegarde : ${backup_branch}"
git fetch origin --prune
git branch "${backup_branch}"

stashed=0
if [ -n "$(git status --porcelain)" ]; then
  print "Modifications non committées trouvées — creation d'un stash temporaire"
  git stash push -u -m "auto-stash-before-sync-${ts}"
  stashed=1
fi

print "Rebase de la branche locale sur origin/main..."
if git rebase origin/main; then
  print "Rebase réussi. Pousser la branche '${branch}' vers origin..."
  git push origin "${branch}"
  print "Push terminé." 
  if [ "$stashed" -eq 1 ]; then
    print "Attention : des modifications ont été stashed. Restaure-les avec 'git stash pop' ou 'git stash list' pour voir le stash créé." 
  fi
  print "Backup branch : ${backup_branch} (contient l'état HEAD avant la synchronisation)."
  exit 0
else
  print "Erreur lors du rebase — arrêt et restauration de l'état avant rebase." >&2
  git rebase --abort || true
  if [ "$stashed" -eq 1 ]; then
    print "Ton travail est stashed (non appliqué). Liste les stashs avec 'git stash list'." 
  fi
  print "La branche de backup '${backup_branch}' contient un snapshot de ton ancien HEAD." 
  print "Résous les conflits manuellement : 'git status' pour voir les fichiers, puis 'git add' + 'git rebase --continue'." 
  exit 3
fi
