from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin, StackedInline
from django.contrib.auth import get_user_model

from store.models import (Customer,
                          Product,
                          ProductPhoto,
                          Cart,
                          Affiliate,
                          Order,
                          ProductsCategory,
                          ProductsSubcategory,
                          ProductReview)

admin.site.register(ProductPhoto)
admin.site.register(Cart)
admin.site.register(Affiliate)
admin.site.register(Order)
admin.site.register(ProductsCategory)


@admin.register(ProductsSubcategory)
class ProductsSubcategoryAdmin(ModelAdmin):
    list_display = [
        'title',
        'category'
    ]


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [
        'title',
        'category',
        'price',
        'rating',
        'picture_count'
    ]

    def picture_count(self, obj):
        return f'{obj.photos.all().count()}'

    picture_count.admin_order_field = 'picture_count'

    fields = [
        'title',
        'slug',
        'category',
        'description',
        'price'
    ]


@admin.register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = (
        'review_id',
        'product',
        'customer',
        'created_date',
        'mark'
    )

    def review_id(self, obj):
        return f'Review#{obj.id}'

    review_id.admin_order_field = 'review_id'
