# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCourseData(TransactionCase):
    """Checks that the course installed correctly and that every quiz is valid."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.channel = cls.env.ref("nova_course_proposal_writing.channel")

    def test_course_is_published(self):
        self.assertTrue(self.channel.is_published)
        self.assertEqual(self.channel.channel_type, "training")

    def test_structure(self):
        slides = self.channel.slide_ids
        self.assertEqual(len(slides.filtered("is_category")), 3, "expected 3 units")
        self.assertEqual(len(slides.filtered(lambda s: not s.is_category)), 10)

    def test_every_lesson_belongs_to_a_unit(self):
        for slide in self.channel.slide_ids.filtered(lambda s: not s.is_category):
            self.assertTrue(slide.category_id, f"{slide.name} has no unit")

    def test_quizzes_are_valid(self):
        questions = self.channel.slide_ids.question_ids
        self.assertEqual(len(questions), 9)
        for question in questions:
            self.assertGreaterEqual(len(question.answer_ids), 2)
            self.assertEqual(len(question.answer_ids.filtered("is_correct")), 1,
                             f"'{question.question}' must have exactly one correct answer")
            self.assertTrue(all(a.comment for a in question.answer_ids), "every answer needs feedback")

    def test_articles_are_rtl(self):
        for slide in self.channel.slide_ids.filtered(lambda s: s.slide_category == "article"):
            self.assertIn('dir="rtl"', slide.html_content or "", f"{slide.name} is not wrapped in RTL")
