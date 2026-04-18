from django.contrib import admin
from .models import Director, Movie, DVD, Order, OrderItem

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(DVD)
admin.site.register(Order)
admin.site.register(OrderItem)
