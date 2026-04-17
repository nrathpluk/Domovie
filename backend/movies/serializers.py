from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name', 'bio', 'nationality', 'birth_year', 'profile_image']


class MovieSerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source='director.name', read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'synopsis', 'release_year', 'genre',
                  'poster_image', 'director', 'director_name', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'content', 'author', 'author_username', 'created_at']
        read_only_fields = ['author', 'created_at']
