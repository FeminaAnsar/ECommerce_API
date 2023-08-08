from .models import Category, Product
from rest_framework import generics
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django_filters import FilterSet, RangeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .serializers import (CategorySerializer, AddProductSerializer,
                          EditProductSerializer,DeleteProductSerializer,
                          ListCategorySerializer,ListProductSerializer,
                          ProductDetailSerializer)


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


class ListCategoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = ListCategorySerializer


class PriceFilter(FilterSet):
    price = RangeFilter()
    class Meta:
        model = Product
        fields = ['price']

# List Product View
class ListProductView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer

    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filterset_class = PriceFilter
    search_fields = ['category__category_name','product_name',]


# Product Detail View
class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
# Create your views here.
