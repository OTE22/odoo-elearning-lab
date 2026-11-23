from odoo import fields, models


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    nova_studio = fields.Json(copy=False, readonly=True)
    # Course landing page: skills, audience, prerequisites, deliverables,
    # FAQ and verified external references (see data/landing.xml).
    nova_landing = fields.Json(copy=False, readonly=True)


class Slide(models.Model):
    _inherit = "slide.slide"

    nova_studio = fields.Json(copy=False, readonly=True)
