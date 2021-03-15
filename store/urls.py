
from rest_framework.routers import SimpleRouter

from store import views

router = SimpleRouter(trailing_slash=False)

router.register('products', views.ProductView, basename='products')
router.register('cart', views.CartView, basename='cart')
router.register('categories', views.ProductsCategoryView, basename='categories')
router.register('subcategories', views.ProductsSubcategoryView, basename='subcategories')
router.register('product-photo', views.ProductPhotoView, basename='product_photos')
urlpatterns = router.urls

urlpatterns += []
