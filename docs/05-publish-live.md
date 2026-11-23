# Publishing the courses live (so anyone can open them)

Goal: a public link such as `https://learn.novatechai.site/slides` where AFH (or anyone) can open the three Arabic courses.

> Odoo Online (the odoo.com SaaS) does **not** allow custom modules. To install these course modules you need your own server (Option A) or Odoo.sh. Option B avoids a server but means re-creating the courses by hand.

## Option A (recommended): a small cloud server with Docker, about 1–2 hours

1. **Rent a server**: Ubuntu 24.04, 2 vCPU, 4 GB RAM (Hetzner, DigitalOcean, Contabo…, roughly USD 5–12 per month).
2. **Point a domain** at it: in your DNS for novatechai.site add an `A` record `learn` → the server's IP.
3. **Install Docker** on the server:
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```
4. **Copy the repo and configure it**:
   ```bash
   git clone https://github.com/<you>/odoo-elearning-lab.git && cd odoo-elearning-lab
   cp .env.example .env && nano .env        # set strong passwords
   nano config/odoo.conf                    # change admin_passwd
   ```
5. **Start and install the three courses**:
   ```bash
   make up && make init
   ```
6. **HTTPS**: get a free certificate, then start the production stack.
   ```bash
   sudo apt install -y certbot
   sudo certbot certonly --standalone -d learn.novatechai.site
   sudo cp /etc/letsencrypt/live/learn.novatechai.site/{fullchain,privkey}.pem ops/nginx/certs/
   sed -i 's/learn.example.org/learn.novatechai.site/g' ops/nginx/odoo.conf
   make down && make prod-up
   ```
7. **Make it public-friendly** (in Odoo, as admin):
   - Change the admin password (top-right avatar → My Profile → Account Security).
   - Website → Settings: name "NovaTechAI Academy", upload the logo, set Arabic as the default language.
   - eLearning → each course: check it is **Published** and enrolment is **Open**.
8. **Add the video lessons**: upload the two lesson MP4s to YouTube as *Unlisted*, then in the course click **Add Content → Video** and paste the YouTube link (place it next to the matching lesson).
9. Open `https://learn.novatechai.site/slides` in a private browser window to check what a visitor sees.

## Option B (no server): Odoo Online, about 1–2 hours per course

1. Create an Odoo Online database at odoo.com with the **eLearning** app (free trial, or check whether Odoo's free one-app plan covers eLearning).
2. Create each course by hand: **eLearning → New course**, add sections (units), then **Add Content → Article**, and paste the lesson text from `addons/<module>/data/course_data.xml` (the text inside each `html_content` field).
3. Add quizzes to the lessons (**Quiz** tab on each lesson) using the questions and answers from the same file.
4. Add the videos as in Option A, step 8.
5. Note: a trial database expires; make sure the link still works while AFH is evaluating.

## Checklist before putting the link in the proposal

- [ ] The link opens without logging in
- [ ] All three courses show, in Arabic, right-to-left
- [ ] Lessons and quizzes open on a phone
- [ ] Video lessons play
- [ ] Admin and master passwords changed
