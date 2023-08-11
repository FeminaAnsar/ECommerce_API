from .models import User,Category, Product
from rest_framework import generics
from .pagination import CustomPagination
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (UserListSerializer,CategorySerializer, AddProductSerializer,
                          EditProductSerializer,DeleteProductSerializer,
                        )


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all().order_by('email')
    serializer_class = UserListSerializer
    pagination_class = CustomPagination


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class AddCategoryView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes= [JWTAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AddProductView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = AddProductSerializer


class EditProductView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = EditProductSerializer


class DeleteProductView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = DeleteProductSerializer


# Create your views here.
