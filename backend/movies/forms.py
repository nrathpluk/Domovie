from django import forms
from .models import Movie, Director


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'synopsis', 'release_year', 'genre', 'poster_image', 'director']


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name', 'bio', 'nationality', 'birth_year', 'profile_image']
