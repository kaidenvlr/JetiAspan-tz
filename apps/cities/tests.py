import json
import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import path, include, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase


class TestProducts(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('apps.cities.urls')),
        path('api/', include('apps.users.urls')),
    ]

    def setUp(self):
        self.username = "user"
        self.password = "Password123@"
        self.token = self.receive_token()

        self.files = []

        filenames = [
            os.path.join(settings.BASE_DIR, 'media/products/cookie.png'),
            os.path.join(settings.BASE_DIR, 'media/products/cookie2.png'),
            os.path.join(settings.BASE_DIR, 'media/products/cookie3.png'),
            os.path.join(settings.BASE_DIR, 'media/products/cookie5.png'),
            os.path.join(settings.BASE_DIR, 'media/products/anothercookie.png'),
            os.path.join(settings.BASE_DIR, 'media/products/cookie400x400.png'),
        ]

        for filename in filenames:
            with open(filename, mode='rb') as f:
                fp = SimpleUploadedFile(name=filename, content=f.read(), content_type='image/png')
                self.files.append(fp)

    def receive_token(self):
        response = self.client.post(reverse('signup'), data={
            "username": self.username,
            "password": self.password,
            "confirm_password": self.password
        })
        self.assertEqual(201, response.status_code)

        response = self.client.post(reverse('token_obtain_pair'), data={
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(200, response.status_code)

        return json.loads(response.content).get('access')

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def create_city(self):
        self.api_authentication()
        # Create city
        response = self.client.post(reverse('city-create'), data={
            "name": "City 1"
        })
        self.assertEqual(201, response.status_code)

    def create_products(self):
        # Create product 1
        response = self.client.post(reverse('product-list'), data={
            "name": "Product 1",
            "price": 100
        })
        self.assertEqual(201, response.status_code)

        # Create product 2
        response = self.client.post(reverse('product-list'), data={
            "name": "Product 2",
            "price": 200
        })
        self.assertEqual(201, response.status_code)

    def create_product_images(self):
        # Create product image
        response = self.client.post(reverse('product-image-create'), data={
            "product": 1,
            "image": self.files[0]
        })
        self.assertEqual(201, response.status_code)

        # Create product image for city
        response = self.client.post(reverse('product-image-create'), data={
            "product": 1,
            "image": self.files[1],
            "preferred_city_id": 1
        })
        self.assertEqual(201, response.status_code)

        # Create product image
        response = self.client.post(reverse('product-image-create'), data={
            "product": 2,
            "image": self.files[2]
        })
        self.assertEqual(201, response.status_code)

    def test_product_get(self):
        self.create_city()
        self.create_products()
        self.create_product_images()
        response = self.client.get(reverse('product-list'))
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        correct_images = [
            '/media/products/cookie3',
            '/media/products/cookie2',
        ]
        for i, product in enumerate(data):
            self.assertIn('id', product)
            self.assertIn('name', product)
            self.assertIn('price', product)
            self.assertIn('images', product)

            self.assertEqual(product['images'][0][:23], correct_images[i])

    def test_product_get_with_city_id(self):
        self.create_city()
        self.create_products()
        self.create_product_images()

        response = self.client.get(reverse('products', {'city_id': 1}))
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        correct_images = [
            '/media/products/cookie3',
            '/media/products/cookie',
        ]
        for i, product in enumerate(data):
            self.assertIn('id', product)
            self.assertIn('name', product)
            self.assertIn('price', product)
            self.assertIn('images', product)

            self.assertEqual(product['images'][0][:23 - i], [correct_images[i]])
