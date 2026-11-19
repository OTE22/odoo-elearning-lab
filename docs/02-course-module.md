# Project 2: A course as an Odoo module

**Goal:** instead of clicking a course together in the UI, ship it as code: versioned in Git, reviewable, installable on any Odoo 17 database with one command.

Module: `addons/nova_course_proposal_writing/`

```
nova_course_proposal_writing/
├── __init__.py
├── __manifest__.py          # name, version, depends, data files
├── data/course_data.xml     # the course, units, lessons and quizzes
├── static/description/icon.png
├── static/img/cover.png     # course cover image
└── tests/test_course_data.py
```

## How the eLearning models fit together

| Model | What it is | Key fields used |
|-------|------------|-----------------|
| `slide.channel` | The course | `name`, `channel_type` (`training`), `enroll`, `visibility`, `description`, `image_1920`, `is_published` |
| `slide.slide` with `is_category=True` | A unit / section | `name`, `sequence` |
| `slide.slide` | A lesson | `slide_category` (`article`, `document`, `video`, `infographic`, `quiz`), `html_content`, `completion_time` (hours), `sequence` |
| `slide.question` | A quiz question on a lesson | `question`, `slide_id` |
| `slide.answer` | An answer | `text_value`, `is_correct`, `comment` (feedback shown to the learner) |

A lesson belongs to the unit that comes **before it by sequence**. That is why every record has an explicit `sequence`.

## Reading `course_data.xml`

```xml
<record id="channel" model="slide.channel">
    <field name="name">كتابة مقترح مشروع ثقافي ناجح</field>
    <field name="channel_type">training</field>
    <field name="image_1920" type="base64" file="nova_course_proposal_writing/static/img/cover.png"/>
    <field name="is_published" eval="True"/>
</record>
```

- `id="channel"` becomes the XML ID `nova_course_proposal_writing.channel`. Other records point to it with `ref="channel"`.
- `type="base64" file=...` loads a binary file from the module.
- `eval="True"` passes a Python value instead of a string.

## Arabic and right-to-left

Every lesson body is wrapped in:

```html
<div dir="rtl" style="text-align:right;">...</div>
```

so it reads correctly even if the website language is English. When the website language is Arabic, Odoo flips the whole layout automatically.

## Exercises

1. Add a new lesson to Unit 2: copy a `slide.slide` record, give it a new `id` and `sequence`, then `make update`.
2. Add a third answer to the SMART lesson question and check that only one is `is_correct`.
3. Change a lesson to `slide_category` `video` and set `url` to a YouTube link. What changes in the player?
