from rest_framework import generics, permissions
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# --- Directors ---

class DirectorListCreateView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAdminOrReadOnly]


class DirectorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAdminOrReadOnly]


# --- Movies ---

class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.select_related('director').order_by('-created_at')
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.select_related('director')
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]


# --- Reviews ---

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.select_related('author').order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
