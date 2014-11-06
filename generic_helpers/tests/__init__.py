# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from generic_helpers.tests.models import (Story, Picture, Comment, Voting)


class TestBase(test.TestCase):
    def setUp(self):
        self.story_1 = Story.objects.create(text='Story #1')
        self.story_2 = Story.objects.create(text='Story #2')
        self.picture_1 = Picture.objects.create(url='http://example.com/1')
        self.picture_2 = Picture.objects.create(url='http://example.com/2')

    def create_comment_for_story1(self):
        return Comment.objects.create(content_object=self.story_1)

    def create_comment_for_story2(self):
        return Comment.objects.create(content_object=self.story_2)

    def create_comment_for_picture1(self):
        return Comment.objects.create(content_object=self.picture_1)


class TestCreate(TestBase):
    def test_create_comment_via_manager(self):
        comment = self.create_comment_for_story1()
        self.assertEquals(1, Comment.objects.count())
        self.assertEquals(self.story_1, comment.content_object)

    def test_create_comment_via_save(self):
        comment = Comment()
        comment.content_object = self.story_1
        comment.save()
        self.assertEquals(1, Comment.objects.count())
        self.assertEquals(self.story_1, comment.content_object)

    def test_get_for_object(self):
        self.create_comment_for_story1()
        test = Comment.objects.get_for_object
        self.assertEquals(1, test(self.story_1).count())
        self.assertEquals(0, test(self.story_2).count())

    def test_get_for_model(self):
        comment_1 = self.create_comment_for_story1()
        comment_2 = self.create_comment_for_story2()
        comment_3 = self.create_comment_for_picture1()

        self.assertEquals(2, Comment.objects.get_for_model(Story).count())
        self.assertIn(comment_1, Comment.objects.get_for_model(Story))
        self.assertIn(comment_2, Comment.objects.get_for_model(Story))
        self.assertIn(comment_3, Comment.objects.get_for_model(Picture))
        self.assertEquals(1, Comment.objects.get_for_model(Picture).count())

    def test_filter_raw(self):
        comment = self.create_comment_for_story1()
        comment_2 = self.create_comment_for_story2()

        qset = Comment.objects.filter(content_object=self.story_1)
        self.assertEquals(1, qset.count())
        self.assertEquals(comment, qset.get())

        qset = Comment.objects.filter(content_object=self.story_2)
        self.assertEquals(1, qset.count())
        self.assertEquals(comment_2, qset.get())

    def test_custom_grm_content_object_name(self):
        Voting.objects.create(buzz=self.story_1)
        self.assertEquals(1, Voting.objects.filter(buzz=self.story_1).count())

    def test_integer_foreign_key(self):
        with self.settings(GENERIC_HELPERS_USE_TEXT_OBJECT_PK=False):
            pass
