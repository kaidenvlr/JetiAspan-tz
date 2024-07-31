from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cities.models import Product, ProductImage
from apps.cities.serializers import ProductSerializer


class ProductAPIView(APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {
            "request": self.request,
            "city_id": self.request.query_params.get('city_id')
        }

    def get(self, request, city_id):
        serializer = self.serializer_class(self.queryset.all(), many=True, context={'request': request, 'city_id': city_id})
        return Response(serializer.data, status=status.HTTP_200_OK)
