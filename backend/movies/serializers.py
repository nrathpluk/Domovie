from rest_framework import serializers
from django.db import transaction

from .models import Director, Movie, DVD, Order, OrderItem


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name', 'bio', 'birth_date']


class MovieSerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source='director.name', read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'synopsis', 'release_date', 'director', 'director_name', 'poster_url']


class DVDSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = DVD
        fields = ['id', 'movie', 'movie_title', 'price', 'stock', 'cover_image']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'dvd', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'items']
        read_only_fields = ['user', 'total_price', 'created_at']


class _OrderItemInputSerializer(serializers.Serializer):
    dvd = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = _OrderItemInputSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must have at least one item.")
        return items

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data['items']

        with transaction.atomic():
            total = 0
            built_items = []

            for item_data in items_data:
                try:
                    dvd = DVD.objects.select_for_update().get(id=item_data['dvd'])
                except DVD.DoesNotExist:
                    raise serializers.ValidationError(
                        f"DVD with id {item_data['dvd']} does not exist."
                    )

                qty = item_data['quantity']
                if dvd.stock < qty:
                    raise serializers.ValidationError(
                        f"Insufficient stock for '{dvd.movie.title}'. Available: {dvd.stock}"
                    )

                dvd.stock -= qty
                dvd.save()
                total += dvd.price * qty
                built_items.append({'dvd': dvd, 'quantity': qty, 'price': dvd.price})

            order = Order.objects.create(user=user, total_price=total)
            for item in built_items:
                OrderItem.objects.create(order=order, **item)

            return order
