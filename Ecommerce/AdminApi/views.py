from .models import User,Category, Product
from UserApi.models import Checkout,OrderedItem
from rest_framework import generics
from .pagination import CustomPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .serializers import CheckoutSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (UserListSerializer,AddCategorySerializer, AddProductSerializer,
                          EditProductSerializer,DeleteProductSerializer,CategorySerializer,
                          OrderConfirmSerializer
                        )
from UserApi.serializers import CheckoutSerializer,OrderedItemSerializer


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

        instance = serializer.instance

        return Response(
            {
                "message": "Category created successfully",
                "category_id": instance.id,
                "category_name": instance.category_name,
            },
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


class PromotionalMail(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        users = User.objects.all()
        subject = 'Independence Day sale Is Live'
        for user in users:
            email_to = [user.email]
            context = {"user":user.username}
            html_content = render_to_string('promotional_mail.html', context)

            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, email_to)
            email.attach_alternative(html_content, 'text/html')
            email.send()

        return Response({'message': 'Promotional emails sent successfully.'})


class OrderListView(generics.ListAPIView):
    queryset = Checkout.objects.all().select_related('user')
    serializer_class = CheckoutSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = CheckoutSerializer(instance)
            items = OrderedItem.objects.filter(checkout=instance)
            order_item_serializer = OrderedItemSerializer(items, many=True)


            ordered_items_list = []
            for item in order_item_serializer.data:
                product = Product.objects.get(id=item['product'])
                ordered_items = {
                    'product': item['product'],
                    'product_name': product.product_name,
                    'quantity': item['quantity'],
                    'subtotal': item['subtotal']
                }
                ordered_items_list.append(ordered_items)

            response_data = {
                'order': serializer.data,
                'order_items': ordered_items_list
            }
            return Response(response_data)
        except Checkout.DoesNotExist:
            return Response({'error': 'Order not found'})



class OrderConfirmView(generics.UpdateAPIView):
    queryset= Checkout.objects.all()
    serializer_class= OrderConfirmSerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[JWTAuthentication]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_status = instance.order_status
        serializer_status = request.data.get('order_status')
        instance.order_status = serializer_status
        instance.save()

        if instance_status != serializer_status:
            context = {

                'order_id': instance.id,
                'order_status': serializer_status
            }

            subject = "Order Status Updated"
            email_to = [instance.user.email]
            html_content = render_to_string('status_update.html', context)
            email = EmailMultiAlternatives(subject, html_content, settings.DEFAULT_FROM_EMAIL, email_to)
            email.attach_alternative(html_content, "text/html")
            email.send()
            return Response({'message': 'Status updated successfully'})
        return Response({'message': 'Status not updated'})

# Create your views here.
