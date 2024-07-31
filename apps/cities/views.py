from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cities.models import Product, City, ProductImage
from apps.cities.serializers import ProductSerializer, CitySerializer, ProductImageSerializer
from apps.common.views import CreateAPIView


class ProductAPIView(APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, city_id):
        serializer = self.serializer_class(self.queryset.all(), many=True,
                                           context={'request': request, 'city_id': city_id})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.all(), many=True,
                                           context={'request': request, 'city_id': None})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityListAPIView(CreateAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class ProductImageAPIView(CreateAPIView):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
