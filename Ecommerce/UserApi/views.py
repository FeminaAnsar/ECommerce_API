from .models import CartList,CartItems,Checkout
from AdminApi.models import Category,User,Product
from rest_framework.views import APIView
from .serializers import (RegisterSerializer,PasswordResetConfirmSerializer,
                          PasswordResetRequestSerializer,CategoryListSerializer,
                          ProductListSerializer,ProductDetailSerializer,AddCartSerializer,
                          CheckoutSerializer,PastOrderSerializer)
from AdminApi.serializers import CartItemsSerializer
from django_filters import FilterSet, RangeFilter,CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.template.loader import render_to_string
from rest_framework import generics, status
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from AdminApi.pagination import CustomPagination


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ResetRequestView(APIView):
    def post(self, request,*args,**kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data["email"])
        reset_token = get_random_string(length=32)  # Generate a reset token
        user.reset_password_token = reset_token
        user.save()

        reset_link = f"http://127.0.0.1:8000/user/reset-password/{reset_token}/"

        email_to = [user.email]
        subject = "Password Reset Request"
        html_content = render_to_string('password_reset_email.html',
                                        {"user": user, "reset_link": reset_link})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, email_to)
        email.attach_alternative(html_content, 'text/html')
        email.send()

        return Response(
            {"message": "Password reset link has been sent to your email."},
            status=status.HTTP_200_OK,
        )


class ResetConfirmView(APIView):
    def post(self, request, reset_token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(reset_password_token=reset_token)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.validated_data["new_password"] != serializer.validated_data["confirm_new_password"]:
            return Response(
                {"error": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.reset_password_token = None
        user.save()

        return Response(
            {"message": "Password reset successful."},
            status=status.HTTP_200_OK,
        )


class CategoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class PriceFilter(FilterSet):
    price = RangeFilter()
    categories__category_name = CharFilter(field_name='categories__category_name')

    class Meta:
        model = Product
        fields = ['price','categories__category_name']


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filterset_class = PriceFilter
    search_fields = ['categories__category_name','product_name']


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class AddCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CartItems.objects.all()
    serializer_class = AddCartSerializer


class CartView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CartItemsSerializer

    def get_queryset(self):
        user = self.request.user
        cart = CartList.objects.filter(user=user).first()
        if cart:
            return CartItems.objects.filter(cart=cart)
        return CartItems.objects.none()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        total_price = sum(
            item.product.price - (item.product.price * item.product.offer / 100) * item.quantity for item in queryset)
        response_data = {
            "cart_items": serializer.data,
            "total_price": total_price
        }
        return Response(response_data)


class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CartItemsSerializer

    def get_queryset(self):
        user = self.request.user
        cart = CartList.objects.filter(user=user).first()
        if cart:
            return CartItems.objects.filter(cart=cart)
        return CartItems.objects.none()

    def perform_update(self, serializer):
        quantity = self.request.data.get('quantity')
        serializer.save(quantity=quantity)


class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        cart = CartList.objects.filter(user=user).first()
        if cart:
            return CartItems.objects.filter(cart=cart)
        return CartItems.objects.none()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Cart Item deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class CheckoutView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer


class ProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, format=None):
        user = self.request.user
        context = {
            'UserID': str(self.request.user.id),
            'Email': str(self.request.user.email),
            'Username': str(self.request.user.username)
        }
        return Response(context)


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self,request):
        logout(request)
        return Response({'message':'Logout Successful'},status=status.HTTP_200_OK)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = PastOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    def get_queryset(self):
        user = self.request.user
        return Checkout.objects.filter(user=user)
