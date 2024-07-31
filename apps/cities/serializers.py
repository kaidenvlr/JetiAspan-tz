from rest_framework import serializers

from django.conf import settings

from apps.cities.models import Product, ProductImage, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'created_at', 'modified_at')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image', 'preferred_city', 'created_at', 'modified_at')


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'images', 'created_at', 'modified_at')

    def get_images(self, obj):
        city_id = self.context.get('city_id')
        qs = ProductImage.objects.filter(preferred_city_id=city_id, product_id=obj.id)
        city_photos = ProductImage.objects.filter(
            preferred_city_id__isnull=True,
            product_id=obj.id
        ) if qs.count() == 0 else qs
        image_urls = [settings.MEDIA_URL + city_photo for city_photo in city_photos.values_list('image', flat=True)]
        return image_urls
