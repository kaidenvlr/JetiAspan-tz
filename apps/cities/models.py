from django.db import models

from apps.common.models import TimeStampedModel


class City(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class ProductImage(TimeStampedModel):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    preferred_city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='preferred_product_images')

    def __str__(self):
        return f"{self.product.name} - {self.image.url}"
