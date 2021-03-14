from decimal import Decimal
from typing import List, Optional

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ValidationError

from store import models


def calculate_product_rating(obj: models.ProductReview) -> None:
    try:
        obj.product.rating = (obj.product.rating + obj.mark) / 2
    except TypeError:
        obj.product.rating = obj.mark
    obj.product.save()


def get_cart(customer: User) -> models.Cart:
    return models.Cart.objects.get(customer=customer)


def add_products_to_cart(products: List[models.Product], cart: models.Cart) -> models.Cart:
    for product in products:
        relation, is_created = models.ProductCartRelation.objects.get_or_create(
            product=product, cart=cart)

        if not is_created:
            relation.count += 1
            relation.save()

    cart.refresh_from_db()
    return cart


def remove_products_from_cart(products: List[models.Product], cart: models.Cart) -> Optional[models.Cart]:
    for product in products:
        try:
            relation = models.ProductCartRelation.objects.get(product=product, cart=cart)
        except models.ProductCartRelation.DoesNotExist:
            raise ValidationError(f'Product {product.slug} is not in the cart',
                                  code=400)
        else:
            relation.delete()
            # relation.save()

    cart.refresh_from_db()
    return cart


def set_product_count_in_cart(product: models.Product, cart: models.Cart, count: int) -> Optional[models.Cart]:
    if count == 0:
        return remove_products_from_cart([product], cart)

    relation = models.ProductCartRelation.objects.get(product=product, cart=cart)
    relation.count = count
    relation.save()

    cart.refresh_from_db()
    return cart
