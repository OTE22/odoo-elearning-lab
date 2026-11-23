# Learning Studio for Odoo 17

## Installation and upgrades

The three Nova course addons own the published lessons, quizzes and channel images. The optional `nova_learning_studio` addon adds their presentation. On an existing installation with the addons mounted, install just the studio in the target database. Replace TARGET_DB with the database name.

```powershell
docker compose run --rm --no-deps odoo odoo -d TARGET_DB -i nova_learning_studio --no-http --max-cron-threads=0 --stop-after-init
docker compose restart odoo
```

For later studio-only releases, use `-u nova_learning_studio`. For the production Compose override that bakes addons into the image, build and roll out that image using the existing deployment configuration before installing the module. A fresh development installation with `make init` installs the studio and its course dependencies.

## Presentation and media ownership

The addon inherits the Odoo 17 course card, course header, course sidebar, curriculum, article and quiz templates. The fullscreen controller calls the standard article handler before rendering the same media panel. Navigation, membership, assessment, course completion and the assigned instructor come from Odoo. Studio metadata is stored in two dedicated JSON fields. Installing the studio on existing courses writes only those fields. An uploaded channel picture remains the primary card image, with a generated cover available as a fallback. The banner is an independent decorative image.

The design uses a shared paper background with plum for proposal writing, indigo for editorial work and teal for event operations. Course labels are HTML text. The lesson map opens with a keyboard-operable disclosure. On a phone the same stages use a text list. Dark preference applies to the new reading panels and motion preference controls hover movement. Films start on demand, with a poster and a written transcript. The films are silent and the narration scripts are visible on screen.

## Generating a course pack

1. Start from a course addon under `addons/nova_course_<key>` with its channel and article records in `data/course_data.xml`. Each article has an objective in its description, a heading and three labelled facts in a definition list. Article IDs connect the generated pack to Odoo.
2. Add the course to `tools/media_profiles.json` and to the studio dependencies. Provide the category, level, colour, icon, language, chosen film lesson and four storyboard scenes. Each scene supplies a heading, focal fact and narration line. The optional diagrams map provides three editorial stages per lesson. Without an override the builder uses the article's own three case facts.
3. Supply a distinct, rights-cleared master at `static/img/workshop.jpg` or set the profile's `artwork` path relative to its addon. Keep the focal subject within the central crop. The builder checks size and duplicate masters and records the objective and visual choice in a per-course brief.
4. Run the build from the repository root. Python and Pillow are required. For films use an FFmpeg build with libx264, Pillow with complex text layout support and an Arabic-capable font.

```powershell
python tools/build_course_media.py --render --font C:/Windows/Fonts/tahoma.ttf
python tools/build_course_media.py
```

The first command also renders the four eight-second film scenes. The second regenerates metadata, diagrams and stills using existing films. Commit the generated `data/media.xml` and `static/media` directories with the addon. End users and the Odoo server need no rendering dependencies. Each pack contains an SVG icon, article diagrams, two WebP crops, a WebP poster, an H.264 MP4 and a JSON brief with the storyboard and script.

The default artwork provider reads local masters. A studio with a licensed image service can supply a provider implementing `source(module, profile)` to `build(args, provider)`. That provider should return a local image path and handle its own credentials, rights and caching. The existing project photos serve as the three supplied masters. The older SMART and phishing videos under `media/` cover earlier lesson objectives and remain independent of these films.

## Verification

In a disposable database install the studio with `--without-demo=all --test-tags=/nova_learning_studio,/nova_course_ai_cultural_work,/nova_course_digital_safety,/nova_course_proposal_writing --stop-after-init`. The tests check course structure and quiz answers, actual media files, rendered disclosures, film controls and transcript presence. In a browser, visit the catalog and open a preview lesson, expand its diagram and narrow the viewport. As a course member, open the selected film lesson in normal and fullscreen modes. In the budget lab, changing the advance from 70% to 85% changes a 280-unit shortfall into a 110-unit surplus.
