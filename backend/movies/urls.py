from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<str:genre>/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('reviews/', views.data_board, name='data_board'),
    path('dvd/', views.dvd_list, name='dvd_list'),
    path('items/', views.items_forsale, name='items_forsale'),
    path('order/', views.list_order, name='list_order'),
]
