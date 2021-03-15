from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from store.models import Product, Cart, ProductsCategory, ProductsSubcategory, ProductPhoto


class ProductSerializer(serializers.ModelSerializer):
    photos = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='store:product_photos-detail'
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'price',
            'photos',

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


class ProductsCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='store:subcategories-detail'
    )

    class Meta:
        model = ProductsCategory
        fields = [
            'id',
            'title',
            'slug',
            'subcategories'
        ]


class ProductsSubcategorySerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='store:categories-detail'
    )
    products = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='store:products-detail'
    )

    class Meta:
        model = ProductsSubcategory
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'products'
        ]


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = '__all__'