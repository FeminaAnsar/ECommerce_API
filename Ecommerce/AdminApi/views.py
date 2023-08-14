from .models import User,Category, Product
from UserApi.models import CartList
from rest_framework import generics
from .pagination import CustomPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework import status,viewsets
from rest_framework.response import Response
from .serializers import OrderListSerializer, OrderDetailSerializer
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


class OrderListView(generics.ListAPIView):
    queryset = CartList.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAdminUser]

class OrderDetailView(generics.RetrieveAPIView):
    queryset = CartList.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminUser]

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


class OrderStatusUpdateView(viewsets.ModelViewSet):
    queryset = CartList.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['patch']

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        order_status = request.data.get('order_status')

        if order_status in dict(CartList.ORDER_STATUS_CHOICES):
            instance.order_status = order_status
            instance.save()
            serializer = self.get_serializer(instance)

            user = User.objects.all()
            subject = ' Order Status Updated'
            html_content = render_to_string('status_update.html', {'title': ' Order Status Updated',
                                                                   'order_status':order_status})
            text_content = strip_tags(html_content)

            email_to = [user.email]
            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, email_to)
            email.attach_alternative(html_content, 'text/html')
            email.send()

            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid order status.'}, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
