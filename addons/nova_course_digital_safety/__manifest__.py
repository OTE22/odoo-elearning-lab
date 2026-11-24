# -*- coding: utf-8 -*-
{
    "name": "Course: Digital Safety for Cultural Organisations (Arabic)",
    "summary": "Advanced Arabic workshop with case exercises and assessed decisions",
    "description": """
Installs a complete Arabic course in Odoo eLearning:
3 units, 5 article lessons (including an advanced lab), 1 lesson quiz and a 5-question final quiz.
Learners assess access, rehearse incident response and validate service recovery.
""",
    "version": "17.0.4.0.0",
    "category": "Website/eLearning",
    "author": "NovaTechAI",
    "website": "https://www.linkedin.com/in/OTE22",
    "license": "LGPL-3",
    "depends": ["website_slides"],
    "data": [
        "data/course_data.xml",
        "data/curriculum.xml",
    ],
    "images": ["static/img/workshop.jpg"],
    "installable": True,
    "application": False,
}
