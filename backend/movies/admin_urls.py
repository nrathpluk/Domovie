from django.urls import path
from . import admin_views

app_name = 'admin_panel'

urlpatterns = [
    path('login/', admin_views.admin_login, name='admin_login'),
    path('', admin_views.dashboard, name='dashboard'),

    path('movies/', admin_views.movies_list, name='movies_list'),
    path('movies/create/', admin_views.movies_create, name='movies_create'),
    path('movies/<int:pk>/edit/', admin_views.movies_edit, name='movies_edit'),
    path('movies/<int:pk>/delete/', admin_views.movies_delete, name='movies_delete'),

    path('directors/', admin_views.directors_list, name='directors_list'),
    path('directors/create/', admin_views.directors_create, name='directors_create'),
    path('directors/<int:pk>/edit/', admin_views.directors_edit, name='directors_edit'),
    path('directors/<int:pk>/delete/', admin_views.directors_delete, name='directors_delete'),

    path('products/', admin_views.products_list, name='products_list'),
    path('products/create/', admin_views.products_create, name='products_create'),
    path('products/<int:pk>/edit/', admin_views.products_edit, name='products_edit'),
    path('products/<int:pk>/delete/', admin_views.products_delete, name='products_delete'),
]
