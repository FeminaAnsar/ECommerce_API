from .models import Category, Product
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .serializers import (CategorySerializer, AddProductSerializer,
                          EditProductSerializer,DeleteProductSerializer,
                        )


class AddCategoryView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AddProductView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = AddProductSerializer


class EditProductView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = EditProductSerializer


class DeleteProductView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = DeleteProductSerializer


# Create your views here.
