from rest_framework import serializers
from AdminApi.models import User,Product,Category
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password','confirm_password']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}, 'email': {'required': True},
                        'username': {'required': True}, 'password': {'write_only': True, 'required': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password does not match.")

        try:
            validate_password(password=password, user=User())

        except serializers.ValidationError as e:
            raise serializers.ValidationError({'password': e})

        return data

    def create(self, validated_data):
        email = self.validated_data['email']
        username=self.validated_data['username']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already taken. Please try another one")

        else:
            password = validated_data.get('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()

            email_to = [user.email]
            subject = 'Registration mail'
            html_content = render_to_string('registration_mail.html',
                                            {'title': 'Registration Email','username': username})
            text_content=strip_tags(html_content)
            email=EmailMultiAlternatives(subject,text_content,settings.DEFAULT_FROM_EMAIL,email_to)
            email.attach_alternative(html_content,'text/html')
            email.send()

            return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class ProductListSerializer(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField()
    categories = CategoryListSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'offer', 'discount_price','categories']

    def get_discount_price(self, obj):
        discount_price = obj.price - (obj.price * obj.offer / 100)
        return discount_price


class ProductDetailSerializer(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'price', 'quantity', 'available', 'image', 'offer', 'discount_price']

    def get_discount_price(self, obj):
        discount_price = obj.price - (obj.price * obj.offer / 100)
        return discount_price
