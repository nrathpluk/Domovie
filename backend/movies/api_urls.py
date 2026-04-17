from django.urls import path
from . import api_views

urlpatterns = [
    path('movies/', api_views.MovieListCreateView.as_view(), name='api_movies'),
    path('movies/<int:pk>/', api_views.MovieDetailView.as_view(), name='api_movie_detail'),
    path('directors/', api_views.DirectorListCreateView.as_view(), name='api_directors'),
    path('directors/<int:pk>/', api_views.DirectorDetailView.as_view(), name='api_director_detail'),
    path('reviews/', api_views.ReviewListCreateView.as_view(), name='api_reviews'),
]
