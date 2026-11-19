# Project 4: Ops toolkit

**Goal:** the things that keep a real eLearning platform alive: backups you can restore, HTTPS, production settings and automatic checks on every push.

## Backups

```bash
make backup                                   # -> backups/elearning_YYYYMMDD_HHMMSS.tar.gz
KEEP_DAYS=14 ./ops/scripts/backup.sh          # also delete archives older than 14 days
make restore FILE=backups/elearning_....tar.gz
```

A backup contains **two** things, and both are needed:

1. `db.dump`: the PostgreSQL database (`pg_dump -Fc`, compressed custom format)
2. `filestore.tar`: course images, PDFs and attachments from `/var/lib/odoo/filestore/<db>`

`restore.sh` asks you to type the database name before it drops anything.

**Practise a restore before you need one.** A backup you never restored is only a hope.

Schedule a nightly backup with cron:

```cron
30 2 * * * cd /opt/odoo-elearning-lab && KEEP_DAYS=14 ./ops/scripts/backup.sh >> backups/backup.log 2>&1
```

## Production with Nginx and HTTPS

```bash
make prod-up
```

`ops/docker-compose.prod.yml` changes the development stack:

| Setting | Why |
|---------|-----|
| No public port on Odoo | Only Nginx is exposed (80/443) |
| `--proxy-mode` | Odoo trusts the `X-Forwarded-*` headers from Nginx |
| `--workers=3` | Multi-process mode; rule of thumb: CPU cores × 2 + 1 |
| `--list-db=False` | Hides the database list from visitors |
| No live addons mount | Runs exactly the code baked into the image |

`ops/nginx/odoo.conf` redirects HTTP to HTTPS, proxies websockets on `/websocket` to port 8072, raises the upload limit for course videos, and turns on gzip for low-bandwidth learners. Put `fullchain.pem` and `privkey.pem` in `ops/nginx/certs/` (for example from Let's Encrypt / certbot).

## Health check

```bash
./ops/scripts/healthcheck.sh https://learn.example.org/web/health
```

The Dockerfile also declares a `HEALTHCHECK`, so `docker compose ps` shows whether Odoo is healthy.

## Continuous integration

`.github/workflows/ci.yml` runs on every push and pull request:

1. **lint:** every XML file parses, Python compiles
2. **odoo-tests:** installs both modules on a fresh Odoo 17 + Postgres 16 and runs the tests
3. **docker-build:** builds the image to catch Dockerfile mistakes

## Exercises

1. Run `make backup`, delete a lesson in the UI, then `make restore` and check the lesson is back.
2. Add a CI step that fails if any image in `addons/` is larger than 500 KB (low-bandwidth rule).
3. Add a `certbot` service to the production compose file to renew certificates automatically.
