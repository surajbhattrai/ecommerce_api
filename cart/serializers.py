from rest_framework import serializers
from rest_framework.fields import Field
from products.serializers import ProductSerializer
from account.serializers import UserSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity' , 'cart']

    def create(self,instance, request):
        cart_obj, created = Cart.objects.get_existing_or_new(request)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(read_only=True, many=True)
    user = UserSerializer()

    class Meta:
        model = Cart
        total = Field(source='total')
        total_cart_products = Field(source='total_cart_products')
        fields = ['id', 'user', 'products', 'total', 'total_cart_products']
        

# class CartSerializer(serializers.ModelSerializer):
#     products = CartItemSerializer(read_only=True, many=True)
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Cart
#         total = Field(source='total')
#         total_cart_products = Field(source='total_cart_products')
#         fields = ['id', 'user', 'products', 'total', 'total_cart_products']