from store.models import ProductReview


def calculate_product_rating(obj: ProductReview):
    try:
        obj.product.rating = (obj.product.rating + obj.mark) / 2
    except TypeError:
        obj.product.rating = obj.mark
    obj.product.save()
