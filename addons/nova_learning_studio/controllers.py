from odoo import http
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class LearningStudio(WebsiteSlides):
    @http.route()
    def get_html_content(self, slide_id):
        result = super().get_html_content(slide_id)
        if result.get("html_content"):
            slide = request.env["slide.slide"].browse(int(slide_id))
            if slide.nova_studio:
                panel = request.env["ir.ui.view"]._render_template(
                    "nova_learning_studio.lesson_media", {"slide": slide}
                )
                result["html_content"] = panel + result["html_content"]
        return result
