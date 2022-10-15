from rest_framework import serializers
from .models import Category , Product , Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields='__all__'
        
 

class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True , many=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model= Product
        fields='__all__'



class ProductWriteSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('category', 'product_name','image', 'price', 'stock')

    # def create(self, validated_data):
    #     category = validated_data.pop('category')
    #     instance, created = Category.objects.get_or_create(**category)
    #     product = Product.objects.create(**validated_data, category=instance)
    #     return product

    # def update(self, instance, validated_data):
    #     if 'category' in validated_data:
    #         nested_serializer = self.fields['category']
    #         nested_instance = instance.category
    #         nested_data = validated_data.pop('category')
    #         nested_serializer.update(nested_instance, nested_data)
    #     return super(ProductWriteSerializer, self).update(instance, validated_data)



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields='__all__'