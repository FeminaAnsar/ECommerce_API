from rest_framework import serializers
from .models import User,Category,Product
from phonenumber_field.serializerfields import PhoneNumberField


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['first_name','last_name','email','registration_date']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category_name']

    def create(self, validated_data):
        category_name = self.validated_data['category_name']
        category = Category.objects.create(**validated_data)
        return category


class AddProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    class Meta:
        model = Product
        fields = ['categories','product_name','description','price','quantity','available','image','offer']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')  # Extract categories data
        product = Product.objects.create(**validated_data)

        # Add categories to the product using set()
        for category in categories_data:
            product.categories.add(category)

        return product


class EditProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [ 'description','price','stock','available', 'image','offer']


class DeleteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'





# List Product Serializer

