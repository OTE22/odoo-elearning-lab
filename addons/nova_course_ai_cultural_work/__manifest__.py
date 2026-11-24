# -*- coding: utf-8 -*-
{
    "name": "Course: AI in Cultural Work: Safe and Responsible Use (Arabic)",
    "summary": "Advanced Arabic workshop with case exercises and assessed decisions",
    "description": """
Installs a complete Arabic course in Odoo eLearning:
3 units, 6 article lessons (including an advanced lab), 2 lesson quizzes and a 6-question final quiz.
Learners produce a bilingual exhibition label and an editorial decision record.
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
