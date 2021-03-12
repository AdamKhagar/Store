from decimal import Decimal

from store.models import ProductReview, Product, Cart


def calculate_product_rating(obj: ProductReview) -> None:
    try:
        obj.product.rating = (obj.product.rating + obj.mark) / 2
    except TypeError:
        obj.product.rating = obj.mark
    obj.product.save()
