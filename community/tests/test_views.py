from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from community.models import Post, Vote

class CommunityViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('community:post_create'), {'title': 'Test Post', 'content': 'This is a test post.'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(str(Post.objects.first()), 'Test Post')

    def test_delete_post_view(self):
        self.client.login(username='testuser', password='testpassword')
        post = Post.objects.create(title='Test Post', content='This is a test post.', posted_by=self.user)
        response = self.client.post(reverse('community:post_delete', args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

    def test_add_comment_view(self):
        self.client.login(username='testuser', password='testpassword')
        post = Post.objects.create(title='Test Post', content='This is a test post.', posted_by=self.user)
        response = self.client.post(reverse('community:add_comment', args=[post.pk]), {'content': 'This is a test comment.'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.comments.count(), 1)

    def test_delete_comment(self):
        self.client.login(username='testuser', password='testpassword')
        post = Post.objects.create(title='Test Post', content='This is a test post.', posted_by=self.user)
        comment = post.comments.create(content='This is a test comment.', commented_by=self.user)
        response = self.client.post(reverse('community:delete_comment', args=[comment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.comments.count(), 0)

    def test_delete_comment_unauthorized(self):
        user = User.objects.create_user(username='testuser2', password='testpassword2')
        self.client.login(username='testuser2', password='testpassword2')
        post = Post.objects.create(title='Test Post', content='This is a test post.', posted_by=self.user)
        response = self.client.post(reverse('community:add_comment', args=[post.pk]), {'content': 'This is a test comment.'})      
        self.assertEqual(post.comments.count(), 1)
        self.assertEqual(post.comments.first().commented_by, response.wsgi_request.user)
        self.client.logout()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('community:delete_comment', args=[Post.objects.first().pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.comments.count(), 1)

    def test_upvote_view(self):
        self.client.login(username='testuser', password='testpassword')
        post = Post.objects.create(title='Test Post', content='This is a test post.', posted_by=self.user)
        response = self.client.post(reverse('community:upvote', args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        vote = Vote.objects.get(post=post, user=self.user)
        self.assertEqual(vote.upvote, True)
        self.assertEqual(vote.downvote, False)
    

    def test_downvote_view(self):
        self.client.login(username='testuser', password='testpassword')
        post = Post.objects.create(title='Test Post', content='This is a test post.', posted_by=self.user)
        response = self.client.post(reverse('community:downvote', args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        vote = Vote.objects.get(post=post, user=self.user)
        self.assertEqual(vote.upvote, False)
        self.assertEqual(vote.downvote, True)
        