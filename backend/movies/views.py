from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Director, Review


def index(request):
    featured_movie = Movie.objects.first()
    featured_director = Director.objects.first()
    return render(request, 'movies/index.html', {
        'featured_movie': featured_movie,
        'featured_director': featured_director,
    })


def genre_list(request):
    return render(request, 'movies/genre_list.html')


def movie_list(request, genre):
    genre_label_map = {'scifi': 'Sci-Fi', 'horror': 'Horror'}
    movies = Movie.objects.filter(genre=genre).select_related('director')
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genre': genre,
        'genre_label': genre_label_map.get(genre, genre),
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})


def data_board(request):
    if request.method == 'POST' and request.user.is_authenticated:
        movie_title = request.POST.get('movie_title', '').strip()
        content = request.POST.get('content', '').strip()
        if movie_title and content:
            Review.objects.create(
                movie_title=movie_title,
                content=content,
                author=request.user,
            )
            messages.success(request, 'โพสต์รีวิวสำเร็จ!')
        return redirect('movies:data_board')

    reviews = Review.objects.select_related('author').order_by('-created_at')
    return render(request, 'movies/data_board.html', {'reviews': reviews})


def dvd_list(request):
    return render(request, 'movies/dvd_list.html')


def items_forsale(request):
    return render(request, 'movies/items_forsale.html')


def list_order(request):
    items = [
        {'name': 'Inception', 'stock': 10},
        {'name': 'Interstellar', 'stock': 10},
        {'name': 'The Matrix', 'stock': 10},
        {'name': 'The Shining', 'stock': 10},
        {'name': 'Encounter', 'stock': 10},
        {'name': 'Blade Runner 2049', 'stock': 10},
        {'name': 'A Quiet Place', 'stock': 10},
        {'name': 'Arrival', 'stock': 10},
        {'name': 'The Conjuring', 'stock': 10},
        {'name': 'The Thing', 'stock': 10},
    ]
    return render(request, 'movies/list_order.html', {'items': items})
