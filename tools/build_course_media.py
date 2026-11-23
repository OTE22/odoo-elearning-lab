"""Build Nova's standalone Odoo media pack from authored course XML and art direction."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "addons/nova_learning_studio"
OUTPUT = MODULE / "static/media"
URL = "/nova_learning_studio/static/media"
ICONS = {
    "proposal": "M5 3h10l4 4v14H5z M14 3v5h5 M8 12h8 M8 16h5",
    "print": "M4 4h13v13H4z M8 20h12V8 M6 14l3-5 3 3 3-5",
    "recovery": "M12 2l8 4v6q0 6-8 10-8-4-8-10V6z M8 12l3 3 5-6",
}


class LocalArtwork:
    """Provider contract: return a distinct, licensed local master for this course."""
    def source(self, module, profile):
        return module / profile.get("artwork", "static/img/workshop.jpg")


def caption(text):
    return escape(text)


def make_diagram(path, heading, pairs, color, lang):
    # Stacked rows stay legible in a small lesson column and in print.
    rtl = lang.startswith("ar")
    x, end = (748, "start") if rtl else (52, "start")
    direction = "rtl" if rtl else "ltr"
    rows = []
    for i, (label, value) in enumerate(pairs):
        y = 86 + i * 94
        rows.append(f'<rect x="32" y="{y}" width="736" height="82" rx="12" fill="white"/>')
        marker = 74 if rtl else 726
        if i < len(pairs) - 1:
            rows.append(f'<path d="M{marker} {y+52}v58" stroke="{color}" stroke-width="3"/>')
        rows.append(f'<circle cx="{marker}" cy="{y+41}" r="12" fill="{color}"/>')
        rows.append(f'<text x="{x}" y="{y+29}" font-size="23" fill="{color}">{caption(label)}</text>')
        rows.append(f'<text x="{x}" y="{y+63}" font-size="29" font-weight="bold">{caption(value)}</text>')
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" lang="{lang}">'
                    f'<title>{caption(heading)}</title><rect width="800" height="400" rx="18" fill="#edf1f2"/>'
                    f'<g direction="{direction}" text-anchor="{end}" font-family="Tahoma,Arial,sans-serif" fill="#1b303b">'
                    f'<text x="{x}" y="57" font-size="32">{caption(heading)}</text>{"".join(rows)}</g></svg>', encoding="utf8")


def make_film(folder, profile, font_path):
    """Render a silent, open-text four-scene explainer. Each scene holds for eight seconds."""
    scene_font = ImageFont.truetype(font_path, 32)
    display = ImageFont.truetype(font_path, 55)
    small = ImageFont.truetype(font_path, 26)
    rtl = profile.get("lang", "ar").startswith("ar")
    edge, anchor, direction = (900, "ra", "rtl") if rtl else (60, "la", "ltr")
    encoder = shutil.which("ffmpeg")
    if not encoder:
        raise RuntimeError("FFmpeg is required to rebuild the films")
    with tempfile.TemporaryDirectory() as temp:
        with tempfile.NamedTemporaryFile(dir=folder, suffix=".mp4", delete=False) as video:
            pending = Path(video.name)
        try:
            for i, (heading, focal, narration) in enumerate(profile["scenes"]):
                frame = Image.new("RGB", (960, 540), "#172a36")
                draw = ImageDraw.Draw(frame)
                draw.rectangle((0, 0, 960, 16), fill=profile["color"])
                for j in range(len(profile["scenes"])):
                    left = 900 - j * 59 - 48 if rtl else 60 + j * 59
                    draw.rounded_rectangle((left, 78, left+48, 85), 3, fill="#ffce88" if j <= i else "#68808a")
                for y, content, font, ink in [(120, heading, scene_font, "#dfede9"), (192, focal, display, "white")]:
                    draw.text((edge, y), content, font=font, fill=ink, anchor=anchor, direction=direction)
                lines = textwrap.wrap(narration, width=57)
                for j, line in enumerate(lines):
                    draw.text((edge, 330 + 46*j), line, font=small, fill="#ebf0f0", anchor=anchor, direction=direction)
                frame.save(Path(temp) / f"{i:02}.png")
                if not i:
                    frame.save(folder / "poster.webp", quality=84)
            subprocess.run([encoder, "-loglevel", "error", "-y", "-framerate", "1/8", "-i", str(Path(temp)/"%02d.png"),
                            "-vf", "fps=24,fade=t=in:st=0:d=0.3", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", str(pending)], check=True)
            pending.replace(folder / "workshop.mp4")
        finally:
            pending.unlink(missing_ok=True)


def metadata(doc, module, record, model, value):
    element = ET.SubElement(doc, "record", id=f"{module}.{record}", model=model, forcecreate="False")
    ET.SubElement(element, "field", name="nova_studio", eval=repr(value))


def build(args, provider):
    profiles = json.loads(Path(args.profiles).read_text(encoding="utf8"))
    doc = ET.Element("odoo")
    digests = set()
    for key, profile in profiles.items():
        module = ROOT / "addons" / ("nova_course_" + key)
        course = ET.parse(module / "data/course_data.xml")
        folder = OUTPUT / key
        folder.mkdir(parents=True, exist_ok=True)
        url = f"{URL}/{key}"
        art = provider.source(module, profile)
        digest = hashlib.sha256(art.read_bytes()).digest()
        if digest in digests:
            raise ValueError(f"{key}: duplicate artwork")
        digests.add(digest)
        with Image.open(art) as photo:
            if photo.width < 960 or photo.height < 440:
                raise ValueError(f"{art}: undersized master")
            for name, size in [("cover", (768, 432)), ("banner", (1200, 440))]:
                ImageOps.fit(photo.convert("RGB"), size).save(folder / f"{name}.webp", quality=82)
        color = profile["color"]
        icon = ICONS[profile["icon"]]
        (folder/"icon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
                                      f'<rect width="24" height="24" rx="5" fill="#f1f4f0"/>'
                                      f'<path d="{icon}" fill="none" stroke="{color}" stroke-width="1.7" '
                                      'stroke-linecap="round" stroke-linejoin="round"/></svg>', encoding="utf8")
        if args.render:
            make_film(folder, profile, args.font)
        for asset in ("poster.webp", "workshop.mp4"):
            if not (folder/asset).is_file():
                raise ValueError(f"Missing {asset} for {key}. Run with --render.")
        outcomes, lessons = [], []
        lang = profile.get("lang", "ar")
        minutes = 0
        for slide in course.findall(".//record[@model='slide.slide']"):
            minutes += round(float(slide.findtext("field[@name='completion_time']", "0")) * 60)
            body = slide.find("field[@name='html_content']/div")
            if body is None:
                continue
            sid = slide.get("id")
            objective = slide.findtext("field[@name='description']")
            heading = body.findtext("h2")
            pairs = [(el.findtext("dt"), el.findtext("dd")) for el in body.findall("dl/div")]
            if len(pairs) != 3 or not all(a and b for a, b in pairs):
                raise ValueError(f"{key}/{sid}: supply three labelled case facts in dl/div")
            if sid in profile.get("diagrams", {}):
                heading, *stages = profile["diagrams"][sid]
                pairs = [stage.split("|", 1) for stage in stages]
                if len(pairs) != 3 or any(len(pair) != 2 for pair in pairs):
                    raise ValueError(f"{key}/{sid}: expected three label|value stages")
            make_diagram(folder/f"{sid}.svg", heading, pairs, color, lang)
            info = {"label": heading, "diagram": f"{url}/{sid}.svg", "steps": [" — ".join(pair) for pair in pairs],
                    "lang": lang, "dir": "rtl" if lang.startswith("ar") else "ltr"}
            if sid == profile["film_lesson"]:
                info.update(film=f"{url}/workshop.mp4", poster=f"{url}/poster.webp", film_title=profile["film_title"],
                            script=[scene[2] for scene in profile["scenes"]])
            metadata(doc, module.name, sid, "slide.slide", info)
            outcomes.append(objective)
            lessons.append({"id": sid, "title": slide.findtext("field[@name='name']"), "objective": objective, "visual": heading})
        if profile["film_lesson"] not in {lesson["id"] for lesson in lessons}:
            raise ValueError(f"{key}: storyboard lesson does not exist")
        channel = course.find(".//record[@id='channel']")
        summary = "".join(channel.find("field[@name='description_short']").itertext()).strip()
        brief = {"title": channel.findtext("field[@name='name']"), "description": summary, "category": profile["category"],
                 "artwork": art.name, "specifications": {"card": "768x432 WebP", "hero": "1200x440 WebP", "film": "960x540 H.264"},
                 "lessons": lessons, "film": profile["film_title"], "storyboard": profile["scenes"], "seconds_per_scene": 8}
        (folder/"brief.json").write_text(json.dumps(brief, ensure_ascii=False, indent=2)+"\n", encoding="utf8")
        duration = f"{minutes} دقيقة" if lang.startswith("ar") else f"{minutes} min"
        metadata(doc, module.name, "channel", "slide.channel", {
            "key": key, "level": profile["level"], "category": profile["category"], "duration": duration,
            "icon": f"{url}/icon.svg", "banner": f"{url}/banner.webp", "cover": f"{url}/cover.webp", "outcomes": outcomes})
    ET.indent(doc)
    path = MODULE/"data/media.xml"
    path.parent.mkdir(exist_ok=True)
    ET.ElementTree(doc).write(path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", default=Path(__file__).with_name("media_profiles.json"))
    parser.add_argument("--render", action="store_true", help="Re-encode the storyboard films")
    parser.add_argument("--font", default=os.environ.get("NOVA_MEDIA_FONT", "C:/Windows/Fonts/tahoma.ttf"))
    build(parser.parse_args(), LocalArtwork())
