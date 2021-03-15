from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store import serializers
from store.models import Product, ProductsCategory, ProductsSubcategory, ProductPhoto
from store.permissions import IsStaffOrReadOnly
from store import services


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = serializers.ProductSerializer


class ProductsCategoryView(ModelViewSet):
    queryset = ProductsCategory.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = serializers.ProductsCategorySerializer


class ProductsSubcategoryView(ModelViewSet):
    queryset = ProductsSubcategory.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = serializers.ProductsSubcategorySerializer


class ProductPhotoView(ModelViewSet):
    queryset = ProductPhoto.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = serializers.ProductPhotoSerializer


class CartView(mixins.ListModelMixin,
               viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('list', 'add_products', 'remove_products'):
            return serializers.CartDetailSerializer
        elif self.action == 'set_product_count':
            return serializers.CartSetProductCountSerializer

    def _add_remove_products(self, request, func):
        cart = services.get_cart(request.user)
        serializer = self.get_serializer(cart, request.data)
        serializer.is_valid(raise_exception=True)
        cart = func(serializer.validated_data.get('products'), cart)

        return Response(self.get_serializer(cart).data,
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        cart = services.get_cart(request.user)
        serializer = self.get_serializer(cart)

        return Response(serializer.data)

    @action(detail=False, url_path='add_products', url_name='add_products', methods=['patch'])
    def add_products(self, request):
        return self._add_remove_products(request, services.add_products_to_cart)

    @action(detail=False, url_path='remove_products', url_name='remove_products', methods=['patch'])
    def remove_products(self, request):
        return self._add_remove_products(request, services.remove_products_from_cart)

    @action(detail=False, url_path='set_product_count', url_name='set_product_count', methods=['patch'])
    def set_product_count(self, request):
        cart = services.get_cart(request.user)
        serializer = self.get_serializer(cart, request.data)
        serializer.is_valid(raise_exception=True)
        cart = services.set_product_count_in_cart(serializer.validated_data.pop('product'),
                                                  cart,
                                                  serializer.validated_data.pop('count'))

        return Response(serializers.CartDetailSerializer(cart).data, status=status.HTTP_200_OK)
