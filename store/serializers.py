from rest_framework.fields import SerializerMethodField
from rest_framework import relations
from rest_framework import serializers

from store.models import Product, Cart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'slug',
            'description',
            'price',

            'rating',
            'category'
        ]


class CartDetailSerializer(serializers.ModelSerializer):
    price = SerializerMethodField('get_price', read_only=True)
    products = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=Product.objects.all())

    def get_price(self, cart):
        return sum([product.price*product.count for product in cart.products.all()])

    class Meta:
        model = Cart
        fields = ['products', 'price']

    def update(self, instance, validated_data):
        products = validated_data.pop('products')

