from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Category, Post


class CategoryAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='123456'
        )

        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )

    def test_get_categories(self):
        url = reverse('category-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_requires_login(self):
        url = reverse('category-list')

        data = {
            'name': 'Science',
            'slug': 'science'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_authenticated(self):
        self.client.login(username='admin', password='123456')

        url = reverse('category-list')

        data = {
            'name': 'Science',
            'slug': 'science'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PostAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='author',
            password='123456'
        )

        self.category = Category.objects.create(
            name='Tech',
            slug='tech'
        )

        self.post = Post.objects.create(
            title='Bai viet dau tien',
            content='Noi dung bai viet',
            author=self.user,
            category=self.category,
            status='published'
        )

    def test_get_posts(self):
        url = reverse('post-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_posts(self):
        url = reverse('post-list') + '?search=dau'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_posts(self):
        url = reverse('post-list') + '?category__slug=tech'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_posts(self):
        url = reverse('post-list') + '?ordering=title'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)