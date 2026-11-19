#!/usr/bin/env bash
# Quick check that Odoo answers. Use it from cron or an uptime monitor.
# Usage: ./ops/scripts/healthcheck.sh [url]
URL="${1:-http://localhost:8069/web/health}"
if curl -fsS --max-time 5 "$URL" > /dev/null; then
  echo "OK  $URL"
else
  echo "DOWN $URL" >&2
  exit 1
fi
