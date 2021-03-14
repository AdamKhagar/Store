from django.urls import path
from rest_framework.routers import SimpleRouter

from store import views

router = SimpleRouter(trailing_slash=False)

router.register('products', views.ProductView, basename='products')
router.register('cart', views.CartView, basename='cart')
urlpatterns = router.urls

urlpatterns += [
    # path('cart/add', views.CartAddProductView.as_view(), name='cart_add'),
    # path('cart', views.CartView.as_view(), name='cart'),
]
