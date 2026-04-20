from django.db import models
from django.conf import settings


class Director(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    synopsis = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    director = models.ForeignKey(
        Director, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies'
    )
    poster_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class DVD(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='dvds')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    cover_image = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.movie.title} DVD"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dvd = models.ForeignKey(DVD, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.dvd}"
