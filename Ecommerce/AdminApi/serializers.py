from rest_framework import serializers
from .models import User,Category,Product
from UserApi.models import CartList, CartItems, Checkout


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['first_name','last_name','email','registration_date']


class AddCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category_name']

    def create(self, validated_data):
        category_name = self.validated_data['category_name']
        category = Category.objects.create(**validated_data)
        return category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','category_name']


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['categories', 'product_name', 'description', 'price', 'stock', 'available', 'image', 'offer']

        def create(self, validated_data):
            product = Product.objects.create(**validated_data)
            return product


class EditProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [ 'categories','product_name','description','price','stock','available', 'image','offer']


class DeleteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['product','product_name', 'quantity','subtotal']

    def get_product_name(self, obj):
        return obj.product.product_name

    def get_subtotal(self, obj):
        discount_price = obj.product.price - (obj.product.price * obj.product.offer / 100)
        return discount_price * obj.quantity


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['mobile', 'address', 'landmark', 'state', 'country', 'pincode', 'payment_amount', 'payment_method']


class OrderListSerializer(serializers.ModelSerializer):
    cart_items = CartItemsSerializer(many=True)
    checkout_info = CheckoutSerializer()

    class Meta:
        model = CartList
        fields = ['id', 'user', 'created_at', 'cart_items', 'checkout_info','order_status']


class OrderDetailSerializer(serializers.ModelSerializer):
    cart_items = CartItemsSerializer(many=True)
    checkout_info = CheckoutSerializer()

    class Meta:
        model = CartList
        fields = ['id', 'user', 'created_at', 'cart_items', 'checkout_info','order_status']


