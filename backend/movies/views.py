import traceback

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

    def get_queryset(self):
        qs = Movie.objects.select_related('director').all().order_by('id')
        director_id = self.request.query_params.get('director')
        if director_id:
            qs = qs.filter(director_id=director_id)
        return qs

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            raise


class DVDViewSet(viewsets.ModelViewSet):
    queryset = DVD.objects.all()
    serializer_class = DVDSerializer
    permission_classes = [IsAdminRoleOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie__title']

    def get_queryset(self):
        qs = DVD.objects.select_related('movie').all().order_by('id')
        movie_id = self.request.query_params.get('movie')
        if movie_id:
            qs = qs.filter(movie_id=movie_id)
        return qs


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items')
            .order_by('-created_at')
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
