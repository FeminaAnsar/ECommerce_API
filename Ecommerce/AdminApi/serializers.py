from rest_framework import serializers
from .models import User,Category,Contact,Product
from phonenumber_field.serializerfields import PhoneNumberField


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category_name']

    def create(self, validated_data):
        category_name = self.validated_data['category_name']
        category = Category.objects.create(**validated_data)
        return category


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['category','product_name','description','price','stock','available','image','offer']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product


class EditProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [ 'description','price','stock','available', 'image','offer']


class DeleteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


# List Product Serializer
class ListProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'offer', 'discount']

    def get_discount(self, obj):
        discount = obj.price - (obj.price * obj.offer / 100)
        return discount


# Product Details Serializer
class ProductDetailSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'price', 'stock', 'available', 'image', 'offer', 'discount']

    def get_discount(self, obj):
        discount = obj.price - (obj.price * obj.offer / 100)
        return discount
