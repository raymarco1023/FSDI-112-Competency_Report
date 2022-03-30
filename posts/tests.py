from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class PostTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            email='test@test.com',
            password='secret'
        )
        self.post = Post.objects.create(
            title='A title',
            body='Content',
            author=self.user
        )

    def test_string_representation(self):
        post = Post(title='Sample title')
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/posts/1/')

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", "A title")
        self.assertEqual("%s" % self.post.author, "test")
        self.assertEqual("{}".format(self.post.body), "Content")

    def test_post_list_view(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content")
        self.assertTemplateUsed(response, "posts/list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_post_detail_view(self):
        response = self.client.get("/post/1/")
        not_found_response = self.client.get("/posts/1000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(not_found_response.status_code, 404)
        self.assertContains(response, "A title")
        self.assertTemplateUsed(response, "posts/detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New content',
            'author': self.user
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.objects.last().text, "New content")

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'text': 'Update content',
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)

# Create your tests here.
