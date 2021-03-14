from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

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


class CartProductsSerializer(serializers.RelatedField):
    def to_representation(self, value):
        product = {
            "id": value.product.id,
            "title": value.product.title,
            "slug": value.product.slug,
            "price": value.product.price,
            "count": value.count,
        }
        return product

    def to_internal_value(self, data):
        try:
            product = Product.objects.get(pk=data)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist')
        else:
            return product


class CartDetailSerializer(serializers.ModelSerializer):
    price = SerializerMethodField('get_price', read_only=True)
    products = CartProductsSerializer(many=True, queryset=Product.objects.all())

    def get_price(self, cart):
        return sum([product.product.price*product.count for product in cart.products.all()])

    class Meta:
        model = Cart
        fields = ['products', 'price']


class CartSetProductCountSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    count = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ['product', 'count']

