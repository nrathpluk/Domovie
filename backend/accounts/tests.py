from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_creates_user(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'testuser',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['role'], 'user')

    def test_login_returns_tokens_with_role(self):
        User.objects.create_user(username='loginuser', password='pass1234')
        response = self.client.post('/api/auth/login/', {
            'username': 'loginuser',
            'password': 'pass1234',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['role'], 'user')
