from django.db import models
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    birth_year = models.IntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='directors/', blank=True, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    GENRE_CHOICES = [
        ('scifi', 'Sci-Fi'),
        ('horror', 'Horror'),
    ]

    title = models.CharField(max_length=200)
    synopsis = models.TextField(blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='scifi')
    poster_image = models.ImageField(upload_to='movies/', blank=True, null=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie_title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie_title} by {self.author.username}"
