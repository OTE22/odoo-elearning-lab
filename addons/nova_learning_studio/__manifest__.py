{
    "name": "Nova Learning Studio",
    "summary": "Course landing pages, artwork, illustrated field notes and motion lessons",
    "version": "17.0.2.0.0",
    "category": "Website/eLearning",
    "license": "LGPL-3",
    "depends": [
        "nova_course_ai_cultural_work",
        "nova_course_digital_safety",
        "nova_course_proposal_writing",
    ],
    "data": ["data/media.xml", "data/landing.xml", "views/studio.xml"],
    "assets": {"web.assets_frontend": [
        "nova_learning_studio/static/src/studio.scss",
        "nova_learning_studio/static/src/studio.js",
    ]},
    "installable": True,
}
