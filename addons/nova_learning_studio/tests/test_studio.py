from pathlib import Path

from lxml import html

from odoo.modules.module import get_module_path
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestMediaPresentation(TransactionCase):
    def test_assets_and_accessible_panels(self):
        root = Path(get_module_path("nova_learning_studio"))
        courses = self.env["slide.channel"].search([("nova_studio", "!=", False)])
        self.assertGreaterEqual(len(courses), 3)
        for course in courses:
            assets = [course.nova_studio[key] for key in ("icon", "cover", "banner")]
            articles = course.slide_ids.filtered(lambda s: s.slide_category == "article")
            # The independent final assignment is assessed with a written rubric.
            course_xmlid = course.get_external_id()[course.id]
            capstone = self.env.ref(course_xmlid.rsplit(".", 1)[0] + ".curriculum_project")
            articles -= capstone
            film_count = 0
            for article in articles:
                presentation = article.nova_studio
                self.assertTrue(presentation)
                panel = self.env["ir.ui.view"]._render_template(
                    "nova_learning_studio.lesson_media", {"slide": article}
                )
                tree = html.fromstring(panel)
                self.assertEqual(tree.xpath("string(.//summary)"), presentation["label"])
                self.assertEqual(len(tree.xpath(".//ol[@class='nova-step-text']/li")), 3)
                assets.append(presentation["diagram"])
                if presentation.get("film"):
                    film_count += 1
                    self.assertTrue(tree.xpath(".//video[@controls]/source"))
                    self.assertEqual(len(presentation["script"]), 4)
                    assets.extend([presentation["film"], presentation["poster"]])
            self.assertEqual(film_count, 1)
            for url in assets:
                self.assertTrue(url.startswith("/nova_learning_studio/static/media/"))
                self.assertTrue((root / url.split("/", 2)[2]).is_file(), url)

    def test_course_landing_pages(self):
        courses = self.env["slide.channel"].search([("nova_landing", "!=", False)])
        self.assertEqual(len(courses), 3)
        for course in courses:
            landing = course.nova_landing
            self.assertEqual(len(landing["skills"]), 6)
            for key in ("audience", "prerequisites", "deliverables", "faq", "references"):
                self.assertGreaterEqual(len(landing[key]), 3, f"{course.name}: {key}")
            for question, answer in landing["faq"]:
                self.assertTrue(question.endswith("؟"), question)
                self.assertTrue(answer)
            for ref in landing["references"]:
                self.assertTrue(ref["url"].startswith("https://"), ref["url"])
                self.assertTrue(ref["title"] and ref["org"])
            page = self.env["ir.ui.view"]._render_template(
                "nova_learning_studio.course_landing", {"channel": course}
            )
            tree = html.fromstring(page)
            self.assertEqual(len(tree.xpath("//section[@id='nova-faq']//details/summary")), len(landing["faq"]))
            links = tree.xpath("//a[@target='_blank']")
            self.assertEqual(len(links), len(landing["references"]))
            self.assertTrue(all("noopener" in a.get("rel", "") for a in links))

    def test_learning_design_layer(self):
        root = Path(get_module_path("nova_learning_studio"))
        courses = self.env["slide.channel"].search([("nova_design", "!=", False)])
        self.assertEqual(len(courses), 3)
        bloom = {"تذكّر", "فهم", "تطبيق", "تحليل", "تقييم", "إبداع"}
        for course in courses:
            design = course.nova_design
            self.assertEqual(len(design["competencies"]), 4)
            self.assertTrue(all(c["level"] in bloom for c in design["competencies"]))
            self.assertEqual(len(design["diagnostic"]), 5)
            self.assertEqual(len(design["flashcards"]), 6)
            self.assertEqual(len(design["glossary"]), 10)
            self.assertEqual(len(design["evaluation"]), 4)
            for item in design["downloads"]:
                path = root / item["file"].split("/nova_learning_studio/", 1)[1]
                self.assertTrue(path.is_file(), item["file"])
                self.assertEqual(path.suffix, ".xlsx")
            top = html.fromstring(self.env["ir.ui.view"]._render_template(
                "nova_learning_studio.course_top", {"channel": course}))
            self.assertEqual(len(top.xpath("//input[@type='checkbox']")), 5)
            self.assertTrue(top.xpath("//output[@aria-live='polite']"))
            for anchor in top.xpath("//nav//a/@href"):
                self.assertTrue(anchor.startswith("#nova-"), anchor)
            page = html.fromstring(self.env["ir.ui.view"]._render_template(
                "nova_learning_studio.course_landing", {"channel": course}))
            self.assertEqual(len(page.xpath("//details[contains(@class,'nova-card')]")), 6)
            self.assertEqual(len(page.xpath("//section[@id='nova-glossary']//tbody/tr")), 10)
            self.assertEqual(len(page.xpath("//a[@download]")), len(design["downloads"]))
            ids = set(page.xpath("//@id")) | set(top.xpath("//@id"))
            for anchor in top.xpath("//nav//a/@href"):
                self.assertIn(anchor[1:], ids, f"{course.name}: broken in-page link {anchor}")
