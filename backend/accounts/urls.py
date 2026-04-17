from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Session-based views (for Django templates / admin panel)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]

# API URL patterns (registered under /api/auth/ in domovie/urls.py)
api_urlpatterns = [
    path('login/', views.api_login, name='api_login'),
    path('logout/', views.api_logout, name='api_logout'),
    path('me/', views.api_me, name='api_me'),
    path('register/', views.api_register, name='api_register'),
]
