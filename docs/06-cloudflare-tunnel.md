# Publishing with Cloudflare Tunnel (free, no server to rent)

Odoo runs in Docker on **your own computer** (or any office machine). Cloudflare Tunnel gives it a public HTTPS address. You don't open ports, buy a server, or set up certificates.

**The one rule:** the computer must stay **on and online** for the link to work. Turn off sleep while AFH is reviewing.

Commands are shown both ways: `make …` (Linux/macOS) and plain `docker compose …` (works everywhere, including Windows with Docker Desktop).

---

## Step 1: Run Odoo with the three courses (about 15 minutes, once)

1. Install **Docker Desktop** (Windows/macOS) or Docker Engine (Linux).
2. Open a terminal in the `odoo-elearning-lab` folder:
   ```bash
   cp .env.example .env          # Windows PowerShell: copy .env.example .env
   ```
   Open `.env` and set a strong `POSTGRES_PASSWORD`.
3. Start and install:
   ```bash
   make up && make init
   ```
   Without make:
   ```bash
   docker compose up -d --build
   docker compose run --rm odoo odoo -d elearning -i nova_course_proposal_writing,nova_course_digital_safety,nova_course_ai_cultural_work --load-language=ar_001 --without-demo=all --stop-after-init
   ```
4. Open http://localhost:8069, log in with `admin` / `admin`, and **change the password right away** (the site is about to be public).

## Step 2a: Quick test link (2 minutes, no account)

```bash
make quick-tunnel
```
Without make:
```bash
docker compose -f docker-compose.yml -f ops/docker-compose.quicktunnel.yml up -d
docker compose -f docker-compose.yml -f ops/docker-compose.quicktunnel.yml logs cloudflared
```
Look for an address like `https://something-random.trycloudflare.com` and open it on your phone.
The address **changes every restart**, so use it to test, not in the proposal.

## Step 2b: Permanent link on your domain (about 20 minutes)

Requirement: `novatechai.site` uses **Cloudflare as its DNS**. If not, add the site in the Cloudflare dashboard (free plan) and change the nameservers at your domain registrar to the two Cloudflare gives you. This can take from a few minutes to a few hours.

1. Cloudflare dashboard → **Zero Trust** → **Networks** → **Tunnels** → **Create a tunnel** → **Cloudflared**. Name it `novatechai-learn`.
2. On the install screen, choose **Docker**. Copy only the **token** (the long text after `--token`).
3. **Public hostname**:
   - Subdomain: `learn` · Domain: `novatechai.site`
   - Service type: `HTTP` · URL: `odoo:8069`
4. Paste the token into `.env`:
   ```
   CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoi...
   ```
5. Start it:
   ```bash
   make tunnel
   ```
   Without make:
   ```bash
   docker compose -f docker-compose.yml -f ops/docker-compose.tunnel.yml up -d
   ```
6. Open **https://learn.novatechai.site/slides**. In Cloudflare the tunnel should show **Healthy**.

## Step 3: Make it look right for visitors

In Odoo, as admin:
- **Website → Configuration → Settings:** site name "NovaTechAI Academy", upload the logo, Arabic as the default language.
- **eLearning:** check each course is **Published** and enrolment is **Open**.
- **Video lessons:** upload the MP4s to YouTube as *Unlisted*, then in the course use **Add Content → Video** with the YouTube link.
- Open the link in a private/incognito window to see what AFH will see.

## Keep it running

- Docker Desktop: Settings → General → **Start Docker Desktop when you sign in**. The containers have `restart: unless-stopped`, so they come back after a reboot.
- Turn off sleep: Windows → Settings → System → Power → Sleep: **Never** (while plugged in).
- If the link stops working: check the PC is on, Docker is running, and the tunnel shows Healthy in Cloudflare.

## Security checklist

- [ ] Admin password changed (not `admin`)
- [ ] `admin_passwd` changed in `config/odoo.conf` (protects the database manager)
- [ ] Never commit `.env` (it contains the tunnel token)
