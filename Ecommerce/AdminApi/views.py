from .models import User,Category, Product
from rest_framework import generics
from .pagination import CustomPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework.response import Response
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


class PromotionalMail(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        users = User.objects.all()
        subject = 'Promotional mail'
        html_content = render_to_string('promotional_mail.html', {'title': 'Promotional Email'})
        text_content = strip_tags(html_content)

        for user in users:
            email_to = [user.email]
            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, email_to)
            email.attach_alternative(html_content, 'text/html')
            email.send()

        return Response({'message': 'Promotional emails sent successfully.'})
# Create your views here.
