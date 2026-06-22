# DoMovie Full-Stack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-ready movie + DVD ordering web app with JWT auth, admin/user roles, search/pagination, and a cart system using localStorage.

**Architecture:** Django 5 REST backend with DRF ViewSets + SimpleJWT; vanilla JS frontend using Fetch API with localStorage for cart/token; PostgreSQL on Neon via dj-database-url; deployed on Render.

**Tech Stack:** Django 5, DRF, SimpleJWT, dj-database-url, django-cors-headers, whitenoise, gunicorn, psycopg2-binary, HTML/CSS/Vanilla JS

---

## File Map

### Backend
```
backend/
  domovie/
    __init__.py
    settings.py       # env-based config, JWT, CORS, pagination, whitenoise
    urls.py           # root URL conf
    wsgi.py
    asgi.py
  accounts/
    __init__.py
    apps.py
    models.py         # CustomUser with role field
    serializers.py    # RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer
    views.py          # register view, CustomTokenObtainPairView
    urls.py           # /auth/register/, /auth/login/, /auth/refresh/
  movies/
    __init__.py
    apps.py
    models.py         # Director, Movie, DVD, Order, OrderItem
    permissions.py    # IsAdminRoleOrReadOnly
    pagination.py     # StandardPagination (page_size=10, max=200)
    serializers.py    # all model serializers + OrderCreateSerializer with atomic logic
    views.py          # DirectorViewSet, MovieViewSet, DVDViewSet, OrderViewSet
    urls.py           # DRF router
    admin.py          # register all models
    migrations/
      __init__.py
  manage.py
```

### Root
```
requirements.txt
.env.example
render.yaml
```

### Frontend
```
frontend/
  css/
    main.css          # all styles: reset, nav, cards, forms, pagination, responsive
  js/
    api.js            # apiFetch wrapper, token header injection, 401 redirect
    auth.js           # getCurrentUser, isLoggedIn, isAdmin, setAuth, logout, requireAuth, requireAdmin
    nav.js            # renderNav() - role-based nav links
    cart.js           # getCart, saveCart, addToCart, removeFromCart, updateCartQuantity, clearCart
    movies.js         # loadMovies, renderPagination, search integration
    dvds.js           # loadDVDs, handleAddToCart, renderPagination, search integration
    orders.js         # loadOrders, requireAuth guard
    admin.js          # loadDirectors, loadMoviesAdmin, loadDVDsAdmin, CRUD + tab switching
  index.html
  login.html
  register.html
  movies.html
  dvds.html
  cart.html
  orders.html
  admin.html
```

---

## Task 1: Project Setup & requirements.txt

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `backend/manage.py`
- Create: `backend/domovie/__init__.py`
- Create: `backend/domovie/wsgi.py`
- Create: `backend/domovie/asgi.py`

- [ ] **Step 1: Create requirements.txt**

```
Django==5.0.6
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
dj-database-url==2.1.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
gunicorn==22.0.0
whitenoise==6.7.0
```

- [ ] **Step 2: Create .env.example**

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

- [ ] **Step 3: Create backend/manage.py**

```python
#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domovie.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Create backend/domovie/__init__.py** (empty file)

- [ ] **Step 5: Create backend/domovie/wsgi.py**

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domovie.settings')
application = get_wsgi_application()
```

- [ ] **Step 6: Create backend/domovie/asgi.py**

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domovie.settings')
application = get_asgi_application()
```

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .env.example backend/
git commit -m "chore: add project skeleton and requirements"
```

---

## Task 2: Django Settings

**Files:**
- Create: `backend/domovie/settings.py`

- [ ] **Step 1: Create backend/domovie/settings.py**

```python
from pathlib import Path
import os
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'accounts',
    'movies',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'domovie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'domovie.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,
    )
}

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'movies.pagination.StandardPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

CORS_ALLOW_ALL_ORIGINS = True
```

- [ ] **Step 2: Create backend/domovie/urls.py**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('movies.urls')),
]
```

- [ ] **Step 3: Commit**

```bash
git add backend/domovie/settings.py backend/domovie/urls.py
git commit -m "feat: add Django settings and root URL config"
```

---

## Task 3: Custom User Model + Auth Endpoints

**Files:**
- Create: `backend/accounts/__init__.py`
- Create: `backend/accounts/apps.py`
- Create: `backend/accounts/models.py`
- Create: `backend/accounts/serializers.py`
- Create: `backend/accounts/views.py`
- Create: `backend/accounts/urls.py`

- [ ] **Step 1: Create backend/accounts/__init__.py** (empty)

- [ ] **Step 2: Create backend/accounts/apps.py**

```python
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
```

- [ ] **Step 3: Create backend/accounts/models.py**

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} ({self.role})"
```

- [ ] **Step 4: Create backend/accounts/serializers.py**

```python
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
        }
        return data
```

- [ ] **Step 5: Create backend/accounts/views.py**

```python
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

- [ ] **Step 6: Create backend/accounts/urls.py**

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, register

urlpatterns = [
    path('register/', register, name='auth-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='auth-login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
]
```

- [ ] **Step 7: Write test for register endpoint**

Create `backend/accounts/tests.py`:

```python
from django.test import TestCase
from django.urls import reverse
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

    def test_login_returns_tokens(self):
        User.objects.create_user(username='loginuser', password='pass1234')
        response = self.client.post('/api/auth/login/', {
            'username': 'loginuser',
            'password': 'pass1234',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['role'], 'user')
```

- [ ] **Step 8: Run migrations and tests**

```bash
cd backend
python manage.py makemigrations accounts
python manage.py migrate
python manage.py test accounts
```

Expected: `OK` — 2 tests pass

- [ ] **Step 9: Commit**

```bash
git add backend/accounts/
git commit -m "feat: add CustomUser model and JWT auth endpoints"
```

---

## Task 4: Movies App — Models

**Files:**
- Create: `backend/movies/__init__.py`
- Create: `backend/movies/apps.py`
- Create: `backend/movies/models.py`
- Create: `backend/movies/admin.py`
- Create: `backend/movies/migrations/__init__.py`

- [ ] **Step 1: Create backend/movies/__init__.py** (empty)

- [ ] **Step 2: Create backend/movies/apps.py**

```python
from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
```

- [ ] **Step 3: Create backend/movies/models.py**

```python
from django.db import models
from django.conf import settings


class Director(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    synopsis = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    director = models.ForeignKey(
        Director, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies'
    )
    poster_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class DVD(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='dvds')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    cover_image = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.movie.title} DVD"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dvd = models.ForeignKey(DVD, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.dvd}"
```

- [ ] **Step 4: Create backend/movies/admin.py**

```python
from django.contrib import admin
from .models import Director, Movie, DVD, Order, OrderItem

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(DVD)
admin.site.register(Order)
admin.site.register(OrderItem)
```

- [ ] **Step 5: Create backend/movies/migrations/__init__.py** (empty)

- [ ] **Step 6: Run migrations**

```bash
cd backend
python manage.py makemigrations movies
python manage.py migrate
```

Expected: migrations created and applied

- [ ] **Step 7: Commit**

```bash
git add backend/movies/
git commit -m "feat: add Director, Movie, DVD, Order, OrderItem models"
```

---

## Task 5: Permissions + Pagination

**Files:**
- Create: `backend/movies/permissions.py`
- Create: `backend/movies/pagination.py`

- [ ] **Step 1: Create backend/movies/permissions.py**

```python
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminRoleOrReadOnly(BasePermission):
    """Allow GET to anyone. POST/PUT/PATCH/DELETE require role=admin."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'
```

- [ ] **Step 2: Create backend/movies/pagination.py**

```python
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200
```

- [ ] **Step 3: Commit**

```bash
git add backend/movies/permissions.py backend/movies/pagination.py
git commit -m "feat: add IsAdminRoleOrReadOnly permission and StandardPagination"
```

---

## Task 6: Serializers + ViewSets (Directors, Movies, DVDs, Orders)

**Files:**
- Create: `backend/movies/serializers.py`
- Create: `backend/movies/views.py`
- Create: `backend/movies/urls.py`

- [ ] **Step 1: Create backend/movies/serializers.py**

```python
from rest_framework import serializers
from django.db import transaction

from .models import Director, Movie, DVD, Order, OrderItem


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name', 'bio', 'birth_date']


class MovieSerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source='director.name', read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'synopsis', 'release_date', 'director', 'director_name', 'poster_url']


class DVDSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = DVD
        fields = ['id', 'movie', 'movie_title', 'price', 'stock', 'cover_image']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'dvd', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'items']
        read_only_fields = ['user', 'total_price', 'created_at']


class _OrderItemInputSerializer(serializers.Serializer):
    dvd = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = _OrderItemInputSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must have at least one item.")
        return items

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data['items']

        with transaction.atomic():
            total = 0
            built_items = []

            for item_data in items_data:
                try:
                    dvd = DVD.objects.select_for_update().get(id=item_data['dvd'])
                except DVD.DoesNotExist:
                    raise serializers.ValidationError(
                        f"DVD with id {item_data['dvd']} does not exist."
                    )

                qty = item_data['quantity']
                if dvd.stock < qty:
                    raise serializers.ValidationError(
                        f"Insufficient stock for '{dvd.movie.title}'. Available: {dvd.stock}"
                    )

                dvd.stock -= qty
                dvd.save()
                total += dvd.price * qty
                built_items.append({'dvd': dvd, 'quantity': qty, 'price': dvd.price})

            order = Order.objects.create(user=user, total_price=total)
            for item in built_items:
                OrderItem.objects.create(order=order, **item)

            return order
```

- [ ] **Step 2: Create backend/movies/views.py**

```python
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Director, Movie, DVD, Order
from .serializers import (
    DirectorSerializer, MovieSerializer, DVDSerializer,
    OrderSerializer, OrderCreateSerializer,
)
from .permissions import IsAdminRoleOrReadOnly


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all().order_by('id')
    serializer_class = DirectorSerializer
    permission_classes = [IsAdminRoleOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.select_related('director').all().order_by('id')
    serializer_class = MovieSerializer
    permission_classes = [IsAdminRoleOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class DVDViewSet(viewsets.ModelViewSet):
    queryset = DVD.objects.select_related('movie').all().order_by('id')
    serializer_class = DVDSerializer
    permission_classes = [IsAdminRoleOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie__title']


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items').order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
```

- [ ] **Step 3: Create backend/movies/urls.py**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DirectorViewSet, MovieViewSet, DVDViewSet, OrderViewSet

router = DefaultRouter()
router.register('directors', DirectorViewSet)
router.register('movies', MovieViewSet)
router.register('dvds', DVDViewSet)
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
```

- [ ] **Step 4: Write tests for movies API**

Create `backend/movies/tests.py`:

```python
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
        response = self.client.post('/api/auth/login/', {'username': user.username, 'password': 'pass'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_unauthenticated_can_list_movies(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_create_director(self):
        self._auth(self.user)
        response = self.client.post('/api/directors/', {'name': 'Test'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_director(self):
        self._auth(self.admin)
        response = self.client.post('/api/directors/', {'name': 'Kubrick', 'bio': '', 'birth_date': None}, format='json')
        self.assertEqual(response.status_code, 201)


class OrderTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='buyer', password='pass', role='user')
        director = Director.objects.create(name='Dir')
        movie = Movie.objects.create(title='Film', director=director)
        self.dvd = DVD.objects.create(movie=movie, price='9.99', stock=5)

    def _auth(self):
        response = self.client.post('/api/auth/login/', {'username': 'buyer', 'password': 'pass'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_create_order_reduces_stock(self):
        self._auth()
        response = self.client.post('/api/orders/', {'items': [{'dvd': self.dvd.id, 'quantity': 2}]}, format='json')
        self.assertEqual(response.status_code, 201)
        self.dvd.refresh_from_db()
        self.assertEqual(self.dvd.stock, 3)

    def test_order_fails_if_insufficient_stock(self):
        self._auth()
        response = self.client.post('/api/orders/', {'items': [{'dvd': self.dvd.id, 'quantity': 10}]}, format='json')
        self.assertEqual(response.status_code, 400)
```

- [ ] **Step 5: Run all tests**

```bash
cd backend
python manage.py test
```

Expected: `OK` — 6 tests pass

- [ ] **Step 6: Commit**

```bash
git add backend/movies/serializers.py backend/movies/views.py backend/movies/urls.py backend/movies/tests.py
git commit -m "feat: add movie/DVD/order ViewSets, serializers, and tests"
```

---

## Task 7: Deployment Files (render.yaml)

**Files:**
- Create: `render.yaml`

- [ ] **Step 1: Create render.yaml**

```yaml
services:
  - type: web
    name: domovie-backend
    env: python
    rootDir: backend
    buildCommand: "pip install -r ../requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput"
    startCommand: "gunicorn domovie.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"
      - key: DATABASE_URL
        fromDatabase:
          name: domovie-db
          property: connectionString

databases:
  - name: domovie-db
    databaseName: domovie
    user: domovie
```

- [ ] **Step 2: Commit**

```bash
git add render.yaml
git commit -m "chore: add render.yaml for Render deployment"
```

---

## Task 8: Frontend — JS Utilities (api.js, auth.js, nav.js, cart.js)

**Files:**
- Create: `frontend/js/api.js`
- Create: `frontend/js/auth.js`
- Create: `frontend/js/nav.js`
- Create: `frontend/js/cart.js`

- [ ] **Step 1: Create frontend/js/api.js**

```javascript
const API_BASE = (() => {
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1') {
        return 'http://localhost:8000/api';
    }
    // Update this URL after deploying to Render
    return 'https://domovie-backend.onrender.com/api';
})();

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers,
    };

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });

        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/login.html';
            return null;
        }

        return response;
    } catch (err) {
        console.error('Network error:', err);
        throw err;
    }
}
```

- [ ] **Step 2: Create frontend/js/auth.js**

```javascript
function getCurrentUser() {
    const data = localStorage.getItem('user');
    return data ? JSON.parse(data) : null;
}

function isLoggedIn() {
    return !!localStorage.getItem('access_token');
}

function isAdmin() {
    const user = getCurrentUser();
    return user !== null && user.role === 'admin';
}

function setAuth(data) {
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('user', JSON.stringify(data.user));
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
    }
}

function requireAdmin() {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }
    if (!isAdmin()) {
        window.location.href = '/index.html';
    }
}
```

- [ ] **Step 3: Create frontend/js/nav.js**

```javascript
function renderNav() {
    const nav = document.getElementById('main-nav');
    if (!nav) return;

    const loggedIn = isLoggedIn();
    const admin = isAdmin();
    const user = getCurrentUser();

    nav.innerHTML = `
        <a href="/index.html" class="brand">DoMovie</a>
        <div class="nav-links">
            <a href="/movies.html">Movies</a>
            <a href="/dvds.html">DVDs</a>
            ${loggedIn ? `
                <a href="/cart.html">Cart</a>
                <a href="/orders.html">My Orders</a>
                ${admin ? '<a href="/admin.html">Admin</a>' : ''}
                <span class="nav-username">${user.username}</span>
                <button class="btn btn-sm" onclick="logout()">Logout</button>
            ` : `
                <a href="/login.html">Login</a>
                <a href="/register.html">Register</a>
            `}
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', renderNav);
```

- [ ] **Step 4: Create frontend/js/cart.js**

```javascript
function getCart() {
    const raw = localStorage.getItem('cart');
    return raw ? JSON.parse(raw) : [];
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(dvdId, quantity = 1) {
    const cart = getCart();
    const existing = cart.find(item => item.dvd === dvdId);
    if (existing) {
        existing.quantity += quantity;
    } else {
        cart.push({ dvd: dvdId, quantity });
    }
    saveCart(cart);
}

function removeFromCart(dvdId) {
    saveCart(getCart().filter(item => item.dvd !== dvdId));
}

function updateCartQuantity(dvdId, quantity) {
    if (quantity <= 0) {
        removeFromCart(dvdId);
        return;
    }
    const cart = getCart();
    const item = cart.find(i => i.dvd === dvdId);
    if (item) {
        item.quantity = quantity;
        saveCart(cart);
    }
}

function clearCart() {
    localStorage.removeItem('cart');
}

function getCartCount() {
    return getCart().reduce((total, item) => total + item.quantity, 0);
}
```

- [ ] **Step 5: Commit**

```bash
git add frontend/js/
git commit -m "feat: add frontend JS utilities (api, auth, nav, cart)"
```

---

## Task 9: Frontend CSS

**Files:**
- Create: `frontend/css/main.css`

- [ ] **Step 1: Create frontend/css/main.css**

```css
:root {
    --primary: #e50914;
    --dark: #141414;
    --darker: #0a0a0a;
    --card-bg: #1f1f1f;
    --text: #ffffff;
    --text-muted: #aaaaaa;
    --border: #333333;
    --success: #28a745;
    --danger: #dc3545;
    --gray: #6c757d;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--dark);
    color: var(--text);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
}

/* ── Nav ── */
nav {
    background-color: var(--darker);
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    border-bottom: 2px solid var(--primary);
    position: sticky;
    top: 0;
    z-index: 100;
}

.brand {
    color: var(--primary);
    font-size: 1.4rem;
    font-weight: 700;
    text-decoration: none;
    letter-spacing: 1px;
    margin-right: auto;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 1.2rem;
}

.nav-links a {
    color: var(--text);
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.2s;
}

.nav-links a:hover {
    color: var(--primary);
}

.nav-username {
    color: var(--text-muted);
    font-size: 0.85rem;
}

/* ── Container ── */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, var(--darker) 0%, #1a0a0a 100%);
    padding: 5rem 2rem;
    text-align: center;
    border-bottom: 1px solid var(--border);
}

.hero h1 {
    font-size: 3.5rem;
    color: var(--primary);
    margin-bottom: 1rem;
    letter-spacing: 2px;
}

.hero p {
    font-size: 1.2rem;
    color: var(--text-muted);
    margin-bottom: 2rem;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

/* ── Buttons ── */
.btn {
    display: inline-block;
    padding: 0.55rem 1.3rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    text-decoration: none;
    transition: opacity 0.2s, transform 0.1s;
    white-space: nowrap;
}

.btn:active { transform: scale(0.98); }
.btn:hover  { opacity: 0.85; }

.btn-primary   { background-color: var(--primary); color: #fff; }
.btn-secondary { background-color: var(--gray);    color: #fff; }
.btn-success   { background-color: var(--success);  color: #fff; }
.btn-danger    { background-color: var(--danger);   color: #fff; }
.btn-sm        { padding: 0.3rem 0.8rem; font-size: 0.8rem; }

/* ── Cards ── */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1.5rem;
}

.card {
    background-color: var(--card-bg);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(229, 9, 20, 0.15);
}

.card img {
    width: 100%;
    height: 300px;
    object-fit: cover;
}

.card-img-placeholder {
    width: 100%;
    height: 300px;
    background: linear-gradient(135deg, #2a2a2a, #1a1a1a);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 3rem;
}

.card-body { padding: 1rem; }

.card-title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
}

.card-text {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-bottom: 0.4rem;
}

.price {
    color: var(--primary);
    font-weight: 700;
    font-size: 1rem !important;
}

/* ── Search ── */
.search-bar {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.search-bar input {
    flex: 1;
    padding: 0.6rem 1rem;
    background-color: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 0.9rem;
    outline: none;
}

.search-bar input:focus { border-color: var(--primary); }

/* ── Pagination ── */
.pagination {
    display: flex;
    gap: 0.4rem;
    justify-content: center;
    margin-top: 2rem;
    flex-wrap: wrap;
}

.pagination button {
    padding: 0.4rem 0.9rem;
    background-color: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    cursor: pointer;
    font-size: 0.85rem;
    transition: background-color 0.2s;
}

.pagination button.active {
    background-color: var(--primary);
    border-color: var(--primary);
}

.pagination button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* ── Forms ── */
.form-container {
    max-width: 420px;
    margin: 4rem auto;
    background-color: var(--card-bg);
    padding: 2rem;
    border-radius: 8px;
}

.form-title {
    font-size: 1.6rem;
    margin-bottom: 1.5rem;
    text-align: center;
}

.form-group { margin-bottom: 1.1rem; }

.form-group label {
    display: block;
    margin-bottom: 0.3rem;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 0.6rem 0.8rem;
    background-color: var(--dark);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 0.9rem;
    outline: none;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus { border-color: var(--primary); }

.form-group textarea { resize: vertical; min-height: 80px; }

.form-footer {
    margin-top: 1rem;
    text-align: center;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.form-footer a { color: var(--primary); text-decoration: none; }

/* ── Alerts ── */
.alert {
    padding: 0.8rem 1rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    display: none;
}

.alert-success {
    background-color: rgba(40, 167, 69, 0.15);
    border: 1px solid var(--success);
    color: var(--success);
}

.alert-error {
    background-color: rgba(220, 53, 69, 0.15);
    border: 1px solid var(--danger);
    color: var(--danger);
}

/* ── Loading / Empty ── */
.loading {
    text-align: center;
    padding: 3rem;
    color: var(--text-muted);
}

.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
}

.empty-state p { margin-bottom: 1rem; font-size: 1.1rem; }

/* ── Table ── */
.table {
    width: 100%;
    border-collapse: collapse;
}

.table th,
.table td {
    padding: 0.8rem 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
}

.table th { color: var(--text-muted); font-weight: 500; }

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-pending   { background: rgba(255,193,7,0.15); color: #ffc107; }
.badge-completed { background: rgba(40,167,69,0.15); color: var(--success); }
.badge-cancelled { background: rgba(220,53,69,0.15); color: var(--danger); }

/* ── Page header ── */
.page-header { margin-bottom: 1.5rem; }
.page-title  { font-size: 1.8rem; margin-bottom: 0.3rem; }
.page-sub    { color: var(--text-muted); font-size: 0.9rem; }

/* ── Cart ── */
.cart-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background-color: var(--card-bg);
    border-radius: 8px;
    margin-bottom: 0.8rem;
}

.cart-item-info { flex: 1; }

.cart-item-title { font-weight: 600; margin-bottom: 0.2rem; }
.cart-item-price { color: var(--primary); font-size: 0.9rem; }

.qty-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.qty-controls button {
    width: 30px;
    height: 30px;
    background-color: var(--border);
    border: none;
    color: var(--text);
    cursor: pointer;
    border-radius: 4px;
    font-size: 1.1rem;
    line-height: 1;
}

.qty-value { min-width: 24px; text-align: center; font-weight: 600; }

.cart-total {
    text-align: right;
    font-size: 1.3rem;
    color: var(--primary);
    font-weight: 700;
    margin: 1.2rem 0;
}

/* ── Admin tabs ── */
.tabs {
    display: flex;
    gap: 0.3rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}

.tab-btn {
    padding: 0.6rem 1.3rem;
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 0.9rem;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    transition: color 0.2s;
}

.tab-btn.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}

.tab-panel { display: none; }
.tab-panel.active { display: block; }

.admin-section { margin-bottom: 2rem; }

.admin-section h3 {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.8rem;
}

/* ── Order items ── */
.order-items {
    padding: 0.5rem 0.5rem 0.5rem 1rem;
    font-size: 0.82rem;
    color: var(--text-muted);
}

/* ── Responsive ── */
@media (max-width: 768px) {
    nav { padding: 0.8rem 1rem; gap: 0.8rem; }
    .nav-links { gap: 0.8rem; }
    .hero h1 { font-size: 2.2rem; }
    .hero { padding: 3rem 1rem; }
    .card-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }
    .container { padding: 1.5rem 1rem; }
    .cart-item { flex-wrap: wrap; }
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/css/main.css
git commit -m "feat: add main CSS (dark theme, cards, forms, nav, responsive)"
```

---

## Task 10: Frontend HTML Pages

**Files:**
- Create: `frontend/index.html`
- Create: `frontend/login.html`
- Create: `frontend/register.html`
- Create: `frontend/movies.html`
- Create: `frontend/dvds.html`
- Create: `frontend/cart.html`
- Create: `frontend/orders.html`
- Create: `frontend/admin.html`

**Frontend JS pages:**
- Create: `frontend/js/movies.js`
- Create: `frontend/js/dvds.js`
- Create: `frontend/js/orders.js`
- Create: `frontend/js/admin.js`

- [ ] **Step 1: Create frontend/index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DoMovie</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav id="main-nav"></nav>

    <div class="hero">
        <h1>DoMovie</h1>
        <p>Discover and order your favourite movies on DVD</p>
        <div class="hero-buttons">
            <a href="/movies.html" class="btn btn-primary">Browse Movies</a>
            <a href="/dvds.html" class="btn btn-secondary">Shop DVDs</a>
        </div>
    </div>

    <div class="container">
        <div class="page-header">
            <h2 class="page-title">Featured Movies</h2>
            <p class="page-sub">A glimpse of our collection</p>
        </div>
        <div class="card-grid" id="featured">
            <div class="loading">Loading…</div>
        </div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/nav.js"></script>
    <script>
        async function loadFeatured() {
            const res = await apiFetch('/movies/?page=1&page_size=4');
            if (!res) return;
            const data = await res.json();
            const movies = data.results || [];
            const grid = document.getElementById('featured');
            if (!movies.length) {
                grid.innerHTML = '<p class="loading">No movies yet.</p>';
                return;
            }
            grid.innerHTML = movies.map(m => `
                <div class="card">
                    ${m.poster_url
                        ? `<img src="${m.poster_url}" alt="${m.title}" loading="lazy">`
                        : '<div class="card-img-placeholder">🎬</div>'
                    }
                    <div class="card-body">
                        <div class="card-title">${m.title}</div>
                        <div class="card-text">${m.director_name || 'Unknown'}</div>
                        <div class="card-text">${m.release_date || ''}</div>
                    </div>
                </div>
            `).join('');
        }
        document.addEventListener('DOMContentLoaded', loadFeatured);
    </script>
</body>
</html>
```

- [ ] **Step 2: Create frontend/login.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login — DoMovie</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav id="main-nav"></nav>

    <div class="form-container">
        <h2 class="form-title">Sign In</h2>
        <div id="alert" class="alert alert-error"></div>

        <form id="login-form">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" required autocomplete="username">
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" required autocomplete="current-password">
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%">Login</button>
        </form>

        <div class="form-footer">
            Don't have an account? <a href="/register.html">Register</a>
        </div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/nav.js"></script>
    <script>
        if (isLoggedIn()) window.location.href = '/index.html';

        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alert = document.getElementById('alert');
            alert.style.display = 'none';

            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            try {
                const res = await fetch(`${API_BASE}/auth/login/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password }),
                });
                const data = await res.json();
                if (res.ok) {
                    setAuth(data);
                    window.location.href = '/index.html';
                } else {
                    alert.textContent = data.detail || 'Invalid credentials.';
                    alert.style.display = 'block';
                }
            } catch (err) {
                alert.textContent = 'Network error. Try again.';
                alert.style.display = 'block';
            }
        });
    </script>
</body>
</html>
```

- [ ] **Step 3: Create frontend/register.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register — DoMovie</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav id="main-nav"></nav>

    <div class="form-container">
        <h2 class="form-title">Create Account</h2>
        <div id="alert" class="alert alert-error"></div>

        <form id="register-form">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" required autocomplete="username">
            </div>
            <div class="form-group">
                <label for="email">Email (optional)</label>
                <input type="email" id="email" autocomplete="email">
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" required autocomplete="new-password" minlength="6">
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%">Register</button>
        </form>

        <div class="form-footer">
            Already have an account? <a href="/login.html">Login</a>
        </div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/nav.js"></script>
    <script>
        if (isLoggedIn()) window.location.href = '/index.html';

        document.getElementById('register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertEl = document.getElementById('alert');
            alertEl.style.display = 'none';

            const payload = {
                username: document.getElementById('username').value.trim(),
                password: document.getElementById('password').value,
                email: document.getElementById('email').value.trim(),
            };

            try {
                const res = await fetch(`${API_BASE}/auth/register/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                const data = await res.json();
                if (res.ok) {
                    setAuth(data);
                    window.location.href = '/index.html';
                } else {
                    const msgs = Object.values(data).flat().join(' ');
                    alertEl.textContent = msgs || 'Registration failed.';
                    alertEl.style.display = 'block';
                }
            } catch (err) {
                alertEl.textContent = 'Network error. Try again.';
                alertEl.style.display = 'block';
            }
        });
    </script>
</body>
</html>
```

- [ ] **Step 4: Create frontend/movies.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movies — DoMovie</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav id="main-nav"></nav>

    <div class="container">
        <div class="page-header">
            <h1 class="page-title">Movies</h1>
            <p class="page-sub">Browse our full collection</p>
        </div>

        <div class="search-bar">
            <input type="text" id="search-input" placeholder="Search by title…">
            <button class="btn btn-primary" id="search-btn">Search</button>
        </div>

        <div class="card-grid" id="movies-grid">
            <div class="loading">Loading movies…</div>
        </div>

        <div class="pagination" id="pagination"></div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/nav.js"></script>
    <script src="/js/movies.js"></script>
</body>
</html>
```

- [ ] **Step 5: Create frontend/js/movies.js**

```javascript
let currentPage = 1;
let currentSearch = '';

async function loadMovies(page, search) {
    const grid = document.getElementById('movies-grid');
    const pager = document.getElementById('pagination');
    grid.innerHTML = '<div class="loading">Loading movies…</div>';

    let url = `/movies/?page=${page}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;

    const res = await apiFetch(url);
    if (!res) return;
    const data = await res.json();

    if (!data.results || !data.results.length) {
        grid.innerHTML = '<div class="empty-state"><p>No movies found.</p></div>';
        pager.innerHTML = '';
        return;
    }

    grid.innerHTML = data.results.map(m => `
        <div class="card">
            ${m.poster_url
                ? `<img src="${m.poster_url}" alt="${m.title}" loading="lazy">`
                : '<div class="card-img-placeholder">🎬</div>'
            }
            <div class="card-body">
                <div class="card-title">${m.title}</div>
                <div class="card-text">${m.director_name || 'Unknown director'}</div>
                <div class="card-text">${m.release_date || ''}</div>
                ${m.synopsis ? `<div class="card-text">${m.synopsis.slice(0, 90)}…</div>` : ''}
            </div>
        </div>
    `).join('');

    renderPagination(data.count, page, pager);
}

function renderPagination(total, page, container) {
    const pages = Math.ceil(total / 10);
    if (pages <= 1) { container.innerHTML = ''; return; }

    const btns = [];
    if (page > 1) btns.push(`<button onclick="go(${page - 1})">‹ Prev</button>`);
    for (let i = 1; i <= pages; i++) {
        btns.push(`<button class="${i === page ? 'active' : ''}" onclick="go(${i})">${i}</button>`);
    }
    if (page < pages) btns.push(`<button onclick="go(${page + 1})">Next ›</button>`);
    container.innerHTML = btns.join('');
}

function go(page) {
    currentPage = page;
    loadMovies(page, currentSearch);
    window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', () => {
    loadMovies(1, '');

    document.getElementById('search-btn').addEventListener('click', () => {
        currentSearch = document.getElementById('search-input').value.trim();
        currentPage = 1;
        loadMovies(1, currentSearch);
    });

    document.getElementById('search-input').addEventListener('keydown', e => {
        if (e.key === 'Enter') document.getElementById('search-btn').click();
    });
});
```

- [ ] **Step 6: Create frontend/dvds.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DVDs — DoMovie</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav id="main-nav"></nav>

    <div class="container">
        <div class="page-header">
            <h1 class="page-title">DVDs</h1>
            <p class="page-sub">Add to cart and checkout</p>
        </div>

        <div id="alert" class="alert alert-success"></div>

        <div class="search-bar">
            <input type="text" id="search-input" placeholder="Search by movie title…">
            <button class="btn btn-primary" id="search-btn">Search</button>
        </div>

        <div class="card-grid" id="dvds-grid">
            <div class="loading">Loading DVDs…</div>
        </div>

        <div class="pagination" id="pagination"></div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/nav.js"></script>
    <script src="/js/cart.js"></script>
    <script src="/js/dvds.js"></script>
</body>
</html>
```

- [ ] **Step 7: Create frontend/js/dvds.js**

```javascript
let currentPage = 1;
let currentSearch = '';

async function loadDVDs(page, search) {
    const grid = document.getElementById('dvds-grid');
    const pager = document.getElementById('pagination');
    grid.innerHTML = '<div class="loading">Loading DVDs…</div>';

    let url = `/dvds/?page=${page}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;

    const res = await apiFetch(url);
    if (!res) return;
    const data = await res.json();

    if (!data.results || !data.results.length) {
        grid.innerHTML = '<div class="empty-state"><p>No DVDs found.</p></div>';
        pager.innerHTML = '';
        return;
    }

    grid.innerHTML = data.results.map(dvd => `
        <div class="card">
            ${dvd.cover_image
                ? `<img src="${dvd.cover_image}" alt="${dvd.movie_title}" loading="lazy">`
                : '<div class="card-img-placeholder">📀</div>'
            }
            <div class="card-body">
                <div class="card-title">${dvd.movie_title}</div>
                <div class="card-text price">$${parseFloat(dvd.price).toFixed(2)}</div>
                <div class="card-text">Stock: ${dvd.stock}</div>
                <div style="margin-top:0.6rem">
                    ${dvd.stock > 0
                        ? `<button class="btn btn-primary btn-sm" onclick="handleAddToCart(${dvd.id})">Add to Cart</button>`
                        : '<span class="badge badge-cancelled">Out of Stock</span>'
                    }
                </div>
            </div>
        </div>
    `).join('');

    renderPagination(data.count, page, pager);
}

function handleAddToCart(dvdId) {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }
    addToCart(dvdId);
    const alertEl = document.getElementById('alert');
    alertEl.textContent = 'Added to cart!';
    alertEl.className = 'alert alert-success';
    alertEl.style.display = 'block';
    setTimeout(() => { alertEl.style.display = 'none'; }, 2500);
}

function renderPagination(total, page, container) {
    const pages = Math.ceil(total / 10);
    if (pages <= 1) { container.innerHTML = ''; return; }

    const btns = [];
    if (page > 1) btns.push(`<button onclick="go(${page - 1})">‹ Prev</button>`);
    for (let i = 1; i <= pages; i++) {
        btns.push(`<button class="${i === page ? 'active' : ''}" onclick="go(${i})">${i}</button>`);
    }
    if (page < pages) btns.push(`<button onclick="go(${page + 1})">Next ›</button>`);
    container.innerHTML = btns.join('');
}

function go(page) {
    currentPage = page;
    loadDVDs(page, currentSearch);
    window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', () => {
    loadDVDs(1, '');

    document.getElementById('search-btn').addEventListener('click', () => {
        currentSearch = document.getElementById('search-input').value.trim();
        currentPage = 1;
        loadDVDs(1, currentSearch);
    });

    document.getElementById('search-input').addEventListener('keydown', e => {
        if (e.key === 'Enter') document.getElementById('search-btn').click();
    });
});
```

- [ ] **Step 8: Create frontend/cart.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cart — DoMovie</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav id="main-nav"></nav>

    <div class="container" style="max-width:700px">
        <div class="page-header">
            <h1 class="page-title">Your Cart</h1>
        </div>

        <div id="alert" class="alert"></div>
        <div id="cart-items">
            <div class="loading">Loading cart…</div>
        </div>
        <div class="cart-total" id="cart-total" style="display:none"></div>
        <div id="checkout-area" style="text-align:right; display:none">
            <button class="btn btn-success" id="checkout-btn" onclick="checkout()">Checkout</button>
        </div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/nav.js"></script>
    <script src="/js/cart.js"></script>
    <script>
        requireAuth();

        let dvdDetails = {};

        async function fetchDVDDetails(ids) {
            const promises = ids.map(id => apiFetch(`/dvds/${id}/`).then(r => r ? r.json() : null));
            const results = await Promise.all(promises);
            results.forEach(dvd => { if (dvd) dvdDetails[dvd.id] = dvd; });
        }

        async function renderCart() {
            const cart = getCart();
            const container = document.getElementById('cart-items');
            const totalEl = document.getElementById('cart-total');
            const checkoutArea = document.getElementById('checkout-area');

            if (!cart.length) {
                container.innerHTML = `
                    <div class="empty-state">
                        <p>Your cart is empty.</p>
                        <a href="/dvds.html" class="btn btn-primary">Browse DVDs</a>
                    </div>`;
                totalEl.style.display = 'none';
                checkoutArea.style.display = 'none';
                return;
            }

            await fetchDVDDetails(cart.map(i => i.dvd));

            let total = 0;
            container.innerHTML = cart.map(item => {
                const dvd = dvdDetails[item.dvd];
                if (!dvd) return '';
                const subtotal = parseFloat(dvd.price) * item.quantity;
                total += subtotal;
                return `
                    <div class="cart-item">
                        <div class="cart-item-info">
                            <div class="cart-item-title">${dvd.movie_title}</div>
                            <div class="cart-item-price">$${parseFloat(dvd.price).toFixed(2)} each</div>
                        </div>
                        <div class="qty-controls">
                            <button onclick="changeQty(${dvd.id}, ${item.quantity - 1})">−</button>
                            <span class="qty-value">${item.quantity}</span>
                            <button onclick="changeQty(${dvd.id}, ${item.quantity + 1})">+</button>
                        </div>
                        <div style="min-width:70px; text-align:right">
                            $${subtotal.toFixed(2)}
                        </div>
                        <button class="btn btn-danger btn-sm" onclick="removeItem(${dvd.id})">✕</button>
                    </div>`;
            }).join('');

            totalEl.textContent = `Total: $${total.toFixed(2)}`;
            totalEl.style.display = 'block';
            checkoutArea.style.display = 'block';
        }

        function changeQty(dvdId, qty) {
            updateCartQuantity(dvdId, qty);
            renderCart();
        }

        function removeItem(dvdId) {
            removeFromCart(dvdId);
            renderCart();
        }

        async function checkout() {
            const cart = getCart();
            if (!cart.length) return;

            const btn = document.getElementById('checkout-btn');
            const alertEl = document.getElementById('alert');
            btn.disabled = true;
            btn.textContent = 'Processing…';

            const res = await apiFetch('/orders/', {
                method: 'POST',
                body: JSON.stringify({ items: cart }),
            });

            if (!res) { btn.disabled = false; btn.textContent = 'Checkout'; return; }

            if (res.ok) {
                clearCart();
                alertEl.textContent = 'Order placed successfully! Redirecting…';
                alertEl.className = 'alert alert-success';
                alertEl.style.display = 'block';
                setTimeout(() => { window.location.href = '/orders.html'; }, 2000);
            } else {
                const err = await res.json();
                const msg = err.non_field_errors || err.detail || JSON.stringify(err);
                alertEl.textContent = Array.isArray(msg) ? msg.join(' ') : msg;
                alertEl.className = 'alert alert-error';
                alertEl.style.display = 'block';
                btn.disabled = false;
                btn.textContent = 'Checkout';
            }
        }

        document.addEventListener('DOMContentLoaded', renderCart);
    </script>
</body>
</html>
```

- [ ] **Step 9: Create frontend/orders.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Orders — DoMovie</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav id="main-nav"></nav>

    <div class="container">
        <div class="page-header">
            <h1 class="page-title">My Orders</h1>
            <p class="page-sub">Your order history</p>
        </div>
        <div id="orders-container">
            <div class="loading">Loading orders…</div>
        </div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/nav.js"></script>
    <script src="/js/orders.js"></script>
</body>
</html>
```

- [ ] **Step 10: Create frontend/js/orders.js**

```javascript
async function loadOrders() {
    requireAuth();
    const container = document.getElementById('orders-container');

    const res = await apiFetch('/orders/');
    if (!res) return;
    const data = await res.json();
    const orders = data.results || data;

    if (!orders.length) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No orders yet.</p>
                <a href="/dvds.html" class="btn btn-primary">Browse DVDs</a>
            </div>`;
        return;
    }

    container.innerHTML = `
        <table class="table">
            <thead>
                <tr>
                    <th>Order</th>
                    <th>Total</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Items</th>
                </tr>
            </thead>
            <tbody>
                ${orders.map(order => `
                    <tr>
                        <td>#${order.id}</td>
                        <td>$${parseFloat(order.total_price).toFixed(2)}</td>
                        <td><span class="badge badge-${order.status}">${order.status}</span></td>
                        <td>${new Date(order.created_at).toLocaleDateString()}</td>
                        <td class="order-items">
                            ${order.items.map(i =>
                                `DVD #${i.dvd} × ${i.quantity} @ $${parseFloat(i.price).toFixed(2)}`
                            ).join(', ')}
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>`;
}

document.addEventListener('DOMContentLoaded', loadOrders);
```

- [ ] **Step 11: Create frontend/admin.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin — DoMovie</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav id="main-nav"></nav>

    <div class="container">
        <div class="page-header">
            <h1 class="page-title">Admin Panel</h1>
        </div>

        <div id="admin-alert" class="alert"></div>

        <div class="tabs">
            <button class="tab-btn active" data-tab="directors">Directors</button>
            <button class="tab-btn" data-tab="movies">Movies</button>
            <button class="tab-btn" data-tab="dvds">DVDs</button>
        </div>

        <!-- DIRECTORS TAB -->
        <div id="tab-directors" class="tab-panel active">
            <div class="admin-section">
                <h3>Add Director</h3>
                <form id="director-form">
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" id="director-name" required>
                    </div>
                    <div class="form-group">
                        <label>Bio</label>
                        <textarea id="director-bio"></textarea>
                    </div>
                    <div class="form-group">
                        <label>Birth Date</label>
                        <input type="date" id="director-birth">
                    </div>
                    <button type="submit" class="btn btn-primary">Add Director</button>
                </form>
            </div>
            <div class="admin-section">
                <h3>Directors List</h3>
                <div id="directors-list"><div class="loading">Loading…</div></div>
            </div>
        </div>

        <!-- MOVIES TAB -->
        <div id="tab-movies" class="tab-panel">
            <div class="admin-section">
                <h3>Add Movie</h3>
                <form id="movie-form">
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" id="movie-title" required>
                    </div>
                    <div class="form-group">
                        <label>Synopsis</label>
                        <textarea id="movie-synopsis"></textarea>
                    </div>
                    <div class="form-group">
                        <label>Release Date</label>
                        <input type="date" id="movie-release">
                    </div>
                    <div class="form-group">
                        <label>Director</label>
                        <select id="movie-director">
                            <option value="">Select Director</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Poster URL (Cloudinary)</label>
                        <input type="url" id="movie-poster" placeholder="https://res.cloudinary.com/…">
                    </div>
                    <button type="submit" class="btn btn-primary">Add Movie</button>
                </form>
            </div>
            <div class="admin-section">
                <h3>Movies List</h3>
                <div id="movies-list"><div class="loading">Loading…</div></div>
            </div>
        </div>

        <!-- DVDS TAB -->
        <div id="tab-dvds" class="tab-panel">
            <div class="admin-section">
                <h3>Add DVD</h3>
                <form id="dvd-form">
                    <div class="form-group">
                        <label>Movie</label>
                        <select id="dvd-movie" required>
                            <option value="">Select Movie</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Price ($)</label>
                        <input type="number" id="dvd-price" step="0.01" min="0" required>
                    </div>
                    <div class="form-group">
                        <label>Stock</label>
                        <input type="number" id="dvd-stock" min="0" required>
                    </div>
                    <div class="form-group">
                        <label>Cover Image URL (Cloudinary)</label>
                        <input type="url" id="dvd-cover" placeholder="https://res.cloudinary.com/…">
                    </div>
                    <button type="submit" class="btn btn-primary">Add DVD</button>
                </form>
            </div>
            <div class="admin-section">
                <h3>DVDs List</h3>
                <div id="dvds-list"><div class="loading">Loading…</div></div>
            </div>
        </div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/nav.js"></script>
    <script src="/js/admin.js"></script>
</body>
</html>
```

- [ ] **Step 12: Create frontend/js/admin.js**

```javascript
document.addEventListener('DOMContentLoaded', () => {
    requireAdmin();

    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
        });
    });

    document.getElementById('director-form').addEventListener('submit', e => { e.preventDefault(); createDirector(); });
    document.getElementById('movie-form').addEventListener('submit', e => { e.preventDefault(); createMovie(); });
    document.getElementById('dvd-form').addEventListener('submit', e => { e.preventDefault(); createDVD(); });

    loadAll();
});

async function loadAll() {
    await Promise.all([loadDirectors(), loadMoviesAdmin(), loadDVDsAdmin()]);
}

// ── Directors ──────────────────────────────────────────────
let directors = [];

async function loadDirectors() {
    const res = await apiFetch('/directors/?page_size=200');
    if (!res) return;
    const data = await res.json();
    directors = data.results || data;
    renderDirectorsList();
    populateDirectorSelect();
}

function renderDirectorsList() {
    const el = document.getElementById('directors-list');
    if (!directors.length) { el.innerHTML = '<div class="empty-state"><p>No directors yet.</p></div>'; return; }
    el.innerHTML = `
        <table class="table">
            <thead><tr><th>Name</th><th>Birth Date</th><th></th></tr></thead>
            <tbody>
                ${directors.map(d => `
                    <tr>
                        <td>${d.name}</td>
                        <td>${d.birth_date || '—'}</td>
                        <td><button class="btn btn-danger btn-sm" onclick="deleteDirector(${d.id})">Delete</button></td>
                    </tr>`).join('')}
            </tbody>
        </table>`;
}

function populateDirectorSelect() {
    document.getElementById('movie-director').innerHTML =
        '<option value="">Select Director</option>' +
        directors.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
}

async function createDirector() {
    const payload = {
        name: document.getElementById('director-name').value.trim(),
        bio: document.getElementById('director-bio').value.trim(),
        birth_date: document.getElementById('director-birth').value || null,
    };
    const res = await apiFetch('/directors/', { method: 'POST', body: JSON.stringify(payload) });
    if (!res) return;
    if (res.ok) {
        showAlert('Director created!', 'success');
        document.getElementById('director-form').reset();
        await loadDirectors();
    } else {
        const err = await res.json();
        showAlert(JSON.stringify(err), 'error');
    }
}

async function deleteDirector(id) {
    if (!confirm('Delete this director?')) return;
    const res = await apiFetch(`/directors/${id}/`, { method: 'DELETE' });
    if (res && res.status === 204) { showAlert('Director deleted.', 'success'); await loadDirectors(); }
}

// ── Movies ────────────────────────────────────────────────
let moviesList = [];

async function loadMoviesAdmin() {
    const res = await apiFetch('/movies/?page_size=200');
    if (!res) return;
    const data = await res.json();
    moviesList = data.results || data;
    renderMoviesList();
    populateMovieSelect();
}

function renderMoviesList() {
    const el = document.getElementById('movies-list');
    if (!moviesList.length) { el.innerHTML = '<div class="empty-state"><p>No movies yet.</p></div>'; return; }
    el.innerHTML = `
        <table class="table">
            <thead><tr><th>Title</th><th>Director</th><th>Release</th><th></th></tr></thead>
            <tbody>
                ${moviesList.map(m => `
                    <tr>
                        <td>${m.title}</td>
                        <td>${m.director_name || '—'}</td>
                        <td>${m.release_date || '—'}</td>
                        <td><button class="btn btn-danger btn-sm" onclick="deleteMovie(${m.id})">Delete</button></td>
                    </tr>`).join('')}
            </tbody>
        </table>`;
}

function populateMovieSelect() {
    document.getElementById('dvd-movie').innerHTML =
        '<option value="">Select Movie</option>' +
        moviesList.map(m => `<option value="${m.id}">${m.title}</option>`).join('');
}

async function createMovie() {
    const payload = {
        title: document.getElementById('movie-title').value.trim(),
        synopsis: document.getElementById('movie-synopsis').value.trim(),
        release_date: document.getElementById('movie-release').value || null,
        director: document.getElementById('movie-director').value || null,
        poster_url: document.getElementById('movie-poster').value.trim(),
    };
    const res = await apiFetch('/movies/', { method: 'POST', body: JSON.stringify(payload) });
    if (!res) return;
    if (res.ok) {
        showAlert('Movie created!', 'success');
        document.getElementById('movie-form').reset();
        populateDirectorSelect();
        await loadMoviesAdmin();
    } else {
        const err = await res.json();
        showAlert(JSON.stringify(err), 'error');
    }
}

async function deleteMovie(id) {
    if (!confirm('Delete this movie?')) return;
    const res = await apiFetch(`/movies/${id}/`, { method: 'DELETE' });
    if (res && res.status === 204) { showAlert('Movie deleted.', 'success'); await loadMoviesAdmin(); }
}

// ── DVDs ──────────────────────────────────────────────────
async function loadDVDsAdmin() {
    const res = await apiFetch('/dvds/?page_size=200');
    if (!res) return;
    const data = await res.json();
    renderDVDsList(data.results || data);
}

function renderDVDsList(dvds) {
    const el = document.getElementById('dvds-list');
    if (!dvds.length) { el.innerHTML = '<div class="empty-state"><p>No DVDs yet.</p></div>'; return; }
    el.innerHTML = `
        <table class="table">
            <thead><tr><th>Movie</th><th>Price</th><th>Stock</th><th></th></tr></thead>
            <tbody>
                ${dvds.map(dvd => `
                    <tr>
                        <td>${dvd.movie_title}</td>
                        <td>$${parseFloat(dvd.price).toFixed(2)}</td>
                        <td>${dvd.stock}</td>
                        <td><button class="btn btn-danger btn-sm" onclick="deleteDVD(${dvd.id})">Delete</button></td>
                    </tr>`).join('')}
            </tbody>
        </table>`;
}

async function createDVD() {
    const payload = {
        movie: document.getElementById('dvd-movie').value,
        price: document.getElementById('dvd-price').value,
        stock: parseInt(document.getElementById('dvd-stock').value),
        cover_image: document.getElementById('dvd-cover').value.trim(),
    };
    if (!payload.movie) { showAlert('Select a movie.', 'error'); return; }
    const res = await apiFetch('/dvds/', { method: 'POST', body: JSON.stringify(payload) });
    if (!res) return;
    if (res.ok) {
        showAlert('DVD created!', 'success');
        document.getElementById('dvd-form').reset();
        populateMovieSelect();
        await loadDVDsAdmin();
    } else {
        const err = await res.json();
        showAlert(JSON.stringify(err), 'error');
    }
}

async function deleteDVD(id) {
    if (!confirm('Delete this DVD?')) return;
    const res = await apiFetch(`/dvds/${id}/`, { method: 'DELETE' });
    if (res && res.status === 204) { showAlert('DVD deleted.', 'success'); await loadDVDsAdmin(); }
}

// ── Alert helper ──────────────────────────────────────────
function showAlert(msg, type) {
    const el = document.getElementById('admin-alert');
    el.textContent = msg;
    el.className = `alert alert-${type}`;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 4000);
}
```

- [ ] **Step 13: Commit**

```bash
git add frontend/
git commit -m "feat: add all frontend HTML pages and JS modules"
```

---

## Self-Review

### Spec coverage

| Requirement | Covered in Task |
|---|---|
| JWT auth (register/login/refresh) | 3 |
| CustomUser with role | 3 |
| Director CRUD (admin only) | 5, 6 |
| Movie CRUD (admin only) | 5, 6 |
| DVD CRUD (admin only) | 5, 6 |
| Order creation with atomic + stock check | 6 |
| User sees own orders only | 6 |
| Pagination (page=10) | 5 (StandardPagination) |
| Search by title | 6 (search_fields) |
| Cart (localStorage) | 8 (cart.js) |
| Add to Cart → redirect if not logged in | 10 (dvds.js) |
| Admin nav hidden for non-admin | 8 (nav.js) |
| Admin page redirects non-admin | 10 (admin.js) |
| Cloudinary URL text fields | 5 (URLField), 10 (admin.html) |
| Render deployment | 7 |
| CORS | 2 (settings) |
| Whitenoise static files | 2 (settings) |

### Gaps found and fixed

- `page_size_query_param` needed for admin to load all records → added to `StandardPagination` in Task 5 ✓
- `OrderViewSet` missing `http_method_names` restriction (no PUT/DELETE on orders) → added in Task 6 ✓
- `tab-panel` CSS needed `.active` class not just `display:none` override → fixed in Task 9 CSS ✓
