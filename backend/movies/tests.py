from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Director, Movie, DVD

User = get_user_model()


class PermissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin', password='pass', role='admin')
        self.user = User.objects.create_user(username='user', password='pass', role='user')

    def _auth(self, user):
        res = self.client.post(
            '/api/auth/login/',
            {'username': user.username, 'password': 'pass'},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def test_unauthenticated_can_list_movies(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_can_list_dvds(self):
        response = self.client.get('/api/dvds/')
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_create_director(self):
        self._auth(self.user)
        response = self.client.post('/api/directors/', {'name': 'Test'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_director(self):
        self._auth(self.admin)
        response = self.client.post(
            '/api/directors/',
            {'name': 'Kubrick', 'bio': '', 'birth_date': None},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Kubrick')


class OrderTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='buyer', password='pass', role='user')
        director = Director.objects.create(name='Dir')
        movie = Movie.objects.create(title='Film', director=director)
        self.dvd = DVD.objects.create(movie=movie, price='9.99', stock=5)

    def _auth(self):
        res = self.client.post(
            '/api/auth/login/',
            {'username': 'buyer', 'password': 'pass'},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def test_unauthenticated_cannot_create_order(self):
        response = self.client.post(
            '/api/orders/',
            {'items': [{'dvd': self.dvd.id, 'quantity': 1}]},
            format='json',
        )
        self.assertEqual(response.status_code, 401)

    def test_create_order_reduces_stock(self):
        self._auth()
        response = self.client.post(
            '/api/orders/',
            {'items': [{'dvd': self.dvd.id, 'quantity': 2}]},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.dvd.refresh_from_db()
        self.assertEqual(self.dvd.stock, 3)
        self.assertEqual(str(response.data['total_price']), '19.98')

    def test_order_fails_if_insufficient_stock(self):
        self._auth()
        response = self.client.post(
            '/api/orders/',
            {'items': [{'dvd': self.dvd.id, 'quantity': 10}]},
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        self.dvd.refresh_from_db()
        self.assertEqual(self.dvd.stock, 5)

    def test_user_sees_only_own_orders(self):
        other_user = User.objects.create_user(username='other', password='pass')
        self._auth()
        self.client.post(
            '/api/orders/',
            {'items': [{'dvd': self.dvd.id, 'quantity': 1}]},
            format='json',
        )
        # other_user has no orders
        res2 = self.client.post(
            '/api/auth/login/',
            {'username': 'other', 'password': 'pass'},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res2.data['access']}")
        response = self.client.get('/api/orders/')
        self.assertEqual(response.data['count'], 0)
