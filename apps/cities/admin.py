from django.contrib import admin

from apps.cities.models import City, Product, ProductImage


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('created_at', 'modified_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    ordering = ('created_at', 'modified_at')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'preferred_city', 'image')
    ordering = ('created_at', 'modified_at')
