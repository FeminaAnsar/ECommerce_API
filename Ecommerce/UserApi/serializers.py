from rest_framework import serializers
from AdminApi.models import User,Product,Category
from UserApi.models import CartItems,CartList,Checkout,OrderedItem
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.password_validation import validate_password
from datetime import timedelta


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
        fields = ['id', 'product_name', 'price','image', 'offer', 'discount_price','categories']

    def get_discount_price(self, obj):
        discount_price = obj.price - (obj.price * obj.offer / 100)
        return discount_price


class ProductDetailSerializer(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'price', 'stock', 'available', 'image', 'offer', 'discount_price']

    def get_discount_price(self, obj):
        discount_price = obj.price - (obj.price * obj.offer / 100)
        return discount_price


class AddCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['product']

    def create(self, validated_data):
        user = self.context['request'].user
        product = self.validated_data['product']
        if CartList.objects.filter(user=user):
            item = CartItems.objects.filter(cart__user=user, product=product).first()
            if item:
                item.quantity += 1
                item.save()
                return item
            else:
                item = CartItems.objects.create(cart=CartList.objects.get(user=user), **validated_data)
                item.save()
                return item
        else:
            cart = CartList.objects.create(user=user)
            cart.save()
            item = CartItems.objects.create(cart=cart, **validated_data)
            item.save()
            return item


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        exclude = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        items = CartItems.objects.filter(cart__user=user)
        total = 0
        ordered_items_data = []
        if items:
            for i in items:
                total += (i.quantity * (i.product.price - (i.product.price * i.product.offer / 100)))
                ordered_items_data.append(
                    {
                     'product': i.product, 'quantity': i.quantity,
                     'subtotal': (i.quantity * (i.product.price - (i.product.price * i.product.offer / 100)))
                     }
                )
            checkout = Checkout.objects.create(user=user, payment_amount=total, **validated_data)

            for item in items:
                product = item.product
                if product.stock < item.quantity:
                    raise serializers.ValidationError(f"Product {product.product_name} is out of stock.")

                product.stock -= item.quantity
                product.save()

            checkout.save()

            OrderedItem.objects.bulk_create(
                [OrderedItem(checkout=checkout, **item_data) for item_data in ordered_items_data]
            )

            items.delete()

            expect_date = checkout.created_at + timedelta(days=10)

            email_to = [user.email]
            subject = 'CheckOut mail'
            html_content = render_to_string('checkout_mail.html',
                                            {'title': 'CheckOut Email','created_at':checkout.created_at,
                                             'expect_date':expect_date,'name':user.username,
                                             'address':checkout.address,'mobile':checkout.mobile,
                                             'payment':checkout.get_payment_method_display(),'total':total})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, email_to)
            email.attach_alternative(html_content, 'text/html')
            email.send()

            email_to = ['admin@gmail.com']
            subject = 'New CheckOut mail'
            html_content = render_to_string('checkout_mail_admin.html',
                                            {'title': 'New CheckOut Email', 'created_at': checkout.created_at,
                                             'expect_date': expect_date, 'name': user.username,
                                             'address': checkout.address, 'mobile': checkout.mobile,
                                             'payment': checkout.get_payment_method_display(), 'total': total})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, email_to)
            email.attach_alternative(html_content, 'text/html')
            email.send()

            return checkout
        raise serializers.ValidationError("No Items for checkout")


class OrderedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = ['product', 'quantity', 'subtotal']


class PastOrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderedItemSerializer(many=True)

    class Meta:
        model = Checkout
        fields = ['id', 'created_at', 'order_status', 'ordered_items']




