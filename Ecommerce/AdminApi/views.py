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
from .serializers import (UserListSerializer,AddCategorySerializer, AddProductSerializer,
                          EditProductSerializer,DeleteProductSerializer,CategorySerializer,
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = instance.id
        user_email = instance.email
        self.perform_destroy(instance)
        return Response(
            {"message": "User deleted successfully", "user_id": user_id, "user_email": user_email},
            status=status.HTTP_204_NO_CONTENT
        )


class AddCategoryView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes= [JWTAuthentication]
    queryset = Category.objects.all()
    serializer_class = AddCategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        category_id = serializer.data['id']
        category_name = serializer.data['category_name']

        return Response(
            {"message": "Category created successfully", "category_id": category_id, "category_name": category_name},
            status=status.HTTP_201_CREATED
        )


class EditCategoryView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product_id = instance.id
        product_name = instance.product_name
        self.perform_destroy(instance)
        return Response(
            {"message": "Product deleted successfully", "product_id": product_id, "product_name": product_name},
            status=status.HTTP_204_NO_CONTENT
        )
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
