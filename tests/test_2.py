import pytest


@pytest.fixture
def story_1(create_model):
    return create_model('Story')(text='Story #1')


@pytest.fixture
def story_2(create_model):
    return create_model('Story')(text='Story #2')


@pytest.fixture
def picture_1(create_model):
    return create_model('Picture')(url='http://example.com/1')


@pytest.fixture
def picture_2(create_model):
    return create_model('Picture')(url='http://example.com/2')


@pytest.fixture
def comment_for_story_1(create_model, story_1):
    return create_model('Comment')(content_object=story_1)


@pytest.fixture
def comment_for_story_2(create_model, story_2):
    return create_model('generic_helpers.Comment')(content_object=story_2)


@pytest.fixture
def comment_for_story_2(create_model, picture_1):
    return create_model('generic_helpers.Comment')(content_object=picture_1)


###

def test_create_comment_via_manager(Comment, story_1):
    comment = Comment.objects.create(content_object=story_1)
    comment.refresh_from_db()

    assert comment.content_object == story_1


def test_create_comment_via_save(Comment, story_1):
    comment = Comment()
    comment.content_object = story_1
    comment.save()

    assert comment.content_object == story_1


@pytest.mark.parametrize('n', [
    ('story_1', 1),
    ('story_2', 0),

])

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
