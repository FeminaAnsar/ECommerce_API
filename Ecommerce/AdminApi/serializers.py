from rest_framework import serializers
from .models import User,Category,Product,Contact
from phonenumber_field.serializerfields import PhoneNumberField
from UserApi.models import CartList, CartItems, Checkout


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['first_name','last_name','email','registration_date']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','category_name']

    def create(self, validated_data):
        category_name = self.validated_data['category_name']
        category = Category.objects.create(**validated_data)
        return category


class AddProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ['categories','product_name','description','price','stock','available','image','offer']

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


class AddContactSerializer(serializers.ModelSerializer):
    mobile = PhoneNumberField(region="IN")
    class Meta:
        model = Contact
        fields = ['user', 'address','mobile']

    def create(self, validated_data):
        user = self.validated_data['user']
        address = self.validated_data['user']
        mobile = self.validated_data['user']
        if Contact.objects.filter(user=user).exists():
            raise serializers.ValidationError('User with contact information is already exist')
        elif Contact.objects.filter(address=address).exists():
            raise serializers.ValidationError('User with this contact already exist')
        else:
            contact = Contact.objects.create(**validated_data)
            return contact


class ListContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id','user','address','mobile']

    def to_representation(self, instance):
        rep = super(ListContactSerializer,self).to_representation(instance)
        rep['user'] = instance.user.username
        return rep


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['product', 'quantity']


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


