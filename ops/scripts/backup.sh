#!/usr/bin/env bash
# Back up the Odoo database AND its filestore (attachments, images) into one archive.
# Usage: ./ops/scripts/backup.sh            -> backups/<db>_<date>.tar.gz
#        KEEP_DAYS=14 ./ops/scripts/backup.sh  (delete archives older than 14 days)
set -euo pipefail
cd "$(dirname "$0")/../.."
source .env

DB="${ODOO_DB:?ODOO_DB missing in .env}"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="backups"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$OUT_DIR"

echo "==> Dumping database '$DB'"
docker compose exec -T db pg_dump -U "$POSTGRES_USER" -Fc "$DB" > "$WORK/db.dump"

echo "==> Copying filestore"
docker compose exec -T odoo tar -C /var/lib/odoo/filestore -cf - "$DB" > "$WORK/filestore.tar" \
  || { echo "   (no filestore yet)"; : > "$WORK/filestore.tar"; }

ARCHIVE="$OUT_DIR/${DB}_${STAMP}.tar.gz"
tar -C "$WORK" -czf "$ARCHIVE" db.dump filestore.tar
echo "==> Saved $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"

if [[ -n "${KEEP_DAYS:-}" ]]; then
  find "$OUT_DIR" -name "${DB}_*.tar.gz" -mtime +"$KEEP_DAYS" -print -delete
fi
