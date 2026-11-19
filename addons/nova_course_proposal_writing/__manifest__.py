# -*- coding: utf-8 -*-
{
    "name": "Course: Writing a Cultural Project Proposal (Arabic)",
    "summary": "Arabic self-paced eLearning course with lessons, practice and quizzes",
    "description": """
Installs a complete Arabic course in Odoo eLearning:
3 units, 5 article lessons, 1 lesson quiz and a 5-question final quiz.
Learning project: shows how to ship course content as an installable Odoo module.
""",
    "version": "17.0.1.0.0",
    "category": "Website/eLearning",
    "author": "NovaTechAI",
    "website": "https://www.linkedin.com/in/OTE22",
    "license": "LGPL-3",
    "depends": ["website_slides"],
    "data": [
        "data/course_data.xml",
    ],
    "images": ["static/img/cover.png"],
    "installable": True,
    "application": False,
}
