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


class DVDViewSet(viewsets.ModelViewSet):
    queryset = DVD.objects.select_related('movie').all().order_by('id')
    serializer_class = DVDSerializer
    permission_classes = [IsAdminRoleOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie__title']


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
