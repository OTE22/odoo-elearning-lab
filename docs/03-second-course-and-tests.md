# Project 3: A second course, plus tests

**Goal:** prove the pattern is reusable (a second course in minutes) and protect it with automated tests.

Module: `addons/nova_course_digital_safety/` (`الأمان الرقمي للمؤسسات الثقافية`)

## Reusing the pattern

The second module has the same structure as Project 2. Only the manifest name and `data/course_data.xml` content change. This is how a team would produce many courses: one template, many content modules.

## The tests

`tests/test_course_data.py` uses Odoo's `TransactionCase`. Each test runs inside a transaction that is rolled back, so tests never leave data behind.

| Test | What it protects against |
|------|--------------------------|
| `test_course_is_published` | Shipping a hidden course |
| `test_structure` | Missing or extra units/lessons |
| `test_every_lesson_belongs_to_a_unit` | Wrong `sequence` values that leave a lesson outside any unit |
| `test_quizzes_are_valid` | Questions with zero or two correct answers, answers without feedback |
| `test_articles_are_rtl` | A lesson that forgot the `dir="rtl"` wrapper |

`@tagged("post_install", "-at_install")` runs the tests after all modules are installed.

## Run them

```bash
make test
```

Expected output ends with:

```
odoo.tests.result: 0 failed, 0 error(s) of 10 tests
```

## Exercises

1. Break a quiz on purpose: set two answers to `is_correct="True"`, run `make test`, read the failure, fix it.
2. Write a new test that checks every lesson has a `completion_time` greater than zero.
3. Create a third course module by copying this one. Which three things must you rename?
