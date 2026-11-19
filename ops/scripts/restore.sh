#!/usr/bin/env bash
# Restore an archive made by backup.sh into the database named in .env.
# WARNING: the existing database with that name is dropped.
# Usage: ./ops/scripts/restore.sh backups/elearning_20261119_101500.tar.gz
set -euo pipefail
cd "$(dirname "$0")/../.."
source .env

ARCHIVE="${1:?usage: restore.sh <backup.tar.gz>}"
DB="${ODOO_DB:?ODOO_DB missing in .env}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

read -r -p "This will REPLACE database '$DB'. Type the database name to continue: " CONFIRM
[[ "$CONFIRM" == "$DB" ]] || { echo "Cancelled."; exit 1; }

tar -C "$WORK" -xzf "$ARCHIVE"

echo "==> Stopping Odoo"
docker compose stop odoo

echo "==> Recreating database"
docker compose exec -T db dropdb -U "$POSTGRES_USER" --if-exists "$DB"
docker compose exec -T db createdb -U "$POSTGRES_USER" "$DB"
docker compose exec -T db pg_restore -U "$POSTGRES_USER" -d "$DB" --no-owner < "$WORK/db.dump"

echo "==> Restoring filestore"
if [[ -s "$WORK/filestore.tar" ]]; then
  docker compose run --rm -T --entrypoint bash odoo -c \
    "rm -rf /var/lib/odoo/filestore/$DB && mkdir -p /var/lib/odoo/filestore && tar -C /var/lib/odoo/filestore -xf -" \
    < "$WORK/filestore.tar"
fi

docker compose start odoo
echo "==> Done. Odoo restarted with the restored data."
