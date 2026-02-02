from django.contrib import admin

# Register your models here.
from .models import Product, CartItem

admin.site.register(Product)
admin.site.register(CartItem)