from django.contrib import admin
from .models import Director, Movie, DVD, Order, OrderItem

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'image_url']
    fields = ['name', 'bio', 'birth_date', 'image_url']

admin.site.register(Movie)
admin.site.register(DVD)
admin.site.register(Order)
admin.site.register(OrderItem)
