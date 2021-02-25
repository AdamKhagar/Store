from store.models import ProductReview


def calculate_product_rating(obj: ProductReview):
    print(obj.product.rating)
    print()
    print('###################################33')
    if not obj.product.rating:
        obj.product.rating = obj.mark
        obj.product.save()

    obj.product.rating = (obj.product.rating + obj.mark) / 2
    obj.product.save()
    print(obj.product.rating, obj.product)
