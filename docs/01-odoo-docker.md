# Project 1: Odoo in Docker

**Goal:** run Odoo 17 and PostgreSQL 16 locally with one command, in a setup you can later take to production.

## The pieces

| File | Role |
|------|------|
| `Dockerfile` | Builds our own image `FROM odoo:17.0`, copies `addons/` and `config/odoo.conf` into it, adds a health check |
| `docker-compose.yml` | Runs two services: `db` (Postgres) and `odoo`, with named volumes so data survives restarts |
| `config/odoo.conf` | Odoo server settings: addons path, data dir, master password, workers |
| `.env` | Secrets and ports (copied from `.env.example`, never committed) |
| `Makefile` | Short commands for everything you do daily |

## Step by step

1. **Copy the environment file and change the passwords**
   ```bash
   cp .env.example .env
   ```
2. **Build and start**
   ```bash
   make up          # = docker compose up -d --build
   docker compose ps
   ```
   `db` must show `healthy` before Odoo starts. That is what `depends_on: condition: service_healthy` does.
3. **Create a database and install the courses**
   ```bash
   make init
   ```
   Under the hood: `odoo -d elearning -i <modules> --load-language=ar_001 --without-demo=all --stop-after-init`.
   - `-i` installs modules (and everything they depend on, here `website_slides`).
   - `--load-language=ar_001` installs Arabic.
   - `--stop-after-init` exits when done instead of serving HTTP.
4. **Open Odoo** at http://localhost:8069 (user `admin`, password `admin`).

## Things to understand

- **Why a custom image?** Production servers should run exactly what you tested. Baking the addons into the image means the same image goes to staging and production.
- **Why mount `./addons` in development?** The volume in `docker-compose.yml` overrides the copied addons, so you can edit files without rebuilding. Run `make update` to reload XML data.
- **Volumes:** `db-data` holds the database, `odoo-data` holds the filestore (attachments, images). Back up **both** (Project 4).
- **Master password** (`admin_passwd` in `odoo.conf`) protects the database manager. Change it.

## Exercises

1. Change `ODOO_PORT` to `8070` in `.env`, run `make up`, and open the new port.
2. Run `make psql` and list courses: `select id, name->>'ar_001' from slide_channel;`
3. Run `make shell` and count lessons: `env['slide.slide'].search_count([('is_category','=',False)])`
