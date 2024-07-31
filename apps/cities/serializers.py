from rest_framework import serializers

from django.conf import settings

from apps.cities.models import Product, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

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
