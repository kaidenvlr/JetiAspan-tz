from django.urls import path
from .views import ProductAPIView

urlpatterns = [
    path('products/<int:city_id>/', ProductAPIView.as_view(), name='products'),
]
