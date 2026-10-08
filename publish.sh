#!/bin/zsh
# Upload the EIS Compass website files (website/) to Xserver.
#
#   ./publish.sh            upload changed files
#   ./publish.sh --dry-run  only list what would be uploaded
#
# Safe by design: nothing on the server is ever deleted. Only EISCompass.html
# and files inside compass/ are added or replaced. Before each upload the live
# EISCompass.html is copied to ~/eis-compass-backups/ (outside public_html).
set -euo pipefail
cd "${0:A:h}"
source ./publish.conf

if [[ "$XSERVER_USER" == "SERVER_ID" || "$XSERVER_HOST" == svXXXX* ]]; then
  echo "Fill in publish.conf first (server ID and host name)."; exit 1
fi

DRY=""
[[ "${1:-}" == "--dry-run" ]] && DRY="-n"
REMOTE="$XSERVER_USER@$XSERVER_HOST"
SSH_CMD="ssh -p 10022 -i $SSH_KEY -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20"

echo "→ Checking the server…"
if ! ${=SSH_CMD} "$REMOTE" "test -f '$REMOTE_DIR/EISCompass.html'"; then
  echo "Stopped: $REMOTE_DIR/EISCompass.html was not found on the server."
  echo "Check REMOTE_DIR in publish.conf."; exit 1
fi

if [[ -z "$DRY" ]]; then
  echo "→ Backing up the live page…"
  ${=SSH_CMD} "$REMOTE" "mkdir -p ~/eis-compass-backups && cp '$REMOTE_DIR/EISCompass.html' ~/eis-compass-backups/EISCompass-\$(date +%Y%m%d-%H%M%S).html && ls -1t ~/eis-compass-backups/EISCompass-*.html | tail -n +31 | xargs -r rm --"
fi

echo "→ Uploading changed files${DRY:+ (dry run — nothing is changed)}…"
rsync -rtzc $DRY --itemize-changes --exclude '.DS_Store' -e "$SSH_CMD" website/ "$REMOTE:$REMOTE_DIR/"

if [[ -z "$DRY" ]]; then
  LOCAL_SUM=$(shasum -a 256 website/EISCompass.html | cut -d' ' -f1)
  REMOTE_SUM=$(${=SSH_CMD} "$REMOTE" "sha256sum '$REMOTE_DIR/EISCompass.html'" | cut -d' ' -f1)
  if [[ "$LOCAL_SUM" == "$REMOTE_SUM" ]]; then
    echo "✓ Done. The live page matches your copy: https://enishi.ac.jp/EISCompass.html"
  else
    echo "⚠ Upload finished, but the live page does not match your copy. Please check."; exit 1
  fi
fi
