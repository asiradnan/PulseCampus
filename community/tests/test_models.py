from django.test import TestCase
from community.models import Post,User,Comment,Vote
from django.core.exceptions import ValidationError

class PostTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(posted_by=self.user, title='Test Post', content='This is a test post.')

    def test_stringify(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_title_cannot_be_empty(self):
        post = Post(posted_by=self.user, title='', content='This is a test post.')
        with self.assertRaises(ValidationError):
            post.full_clean()

class CommentTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(posted_by=self.user, title='Test Post', content='This is a test post.')
        self.comment = Comment.objects.create(post=self.post, commented_by=self.user, content='This is a test comment.')

    def test_stringify(self):
        self.assertEqual(str(self.comment), 'This is a test comment.')

class VoteTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(posted_by=self.user, title='Test Post', content='This is a test post.')
        self.vote = Vote.objects.create(post=self.post, user=self.user, upvote=True, downvote=False)

    def test_upvote_and_downvote_cannot_be_true_simultaneously(self):
        vote = Vote(post=self.post, user=self.user, upvote=True, downvote=True)
        with self.assertRaises(ValidationError):
            vote.full_clean()