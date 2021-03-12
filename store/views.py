from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.models import Product, ProductsCategory, ProductsSubcategory, Cart
from store import serializers


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductsCategoryView(ModelViewSet):
    queryset = ProductsCategory.objects.all()


class ProductsSubcategoryView(ModelViewSet):
    queryset = ProductsSubcategory.objects.all()


# I use GenericAPIView because i want see all parameters in swagger
class CartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartDetailSerializer

    def get_cart(self, customer):
        return Cart.objects.get(customer=customer)

    def get(self, request):
        cart = self.get_cart(customer=request.user)
        return Response(self.get_serializer(cart).data)

    def patch(self, request):
        cart = self.get_cart(customer=request.user)
        serializer = self.get_serializer(cart, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
