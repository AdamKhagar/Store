from django.db import models


class ProductReviewManager(models.Manager):
    def create(self, *args, **kwargs):
        print('create')
        from store.services import calculate_product_rating

        review = super().create(*args, **kwargs)
        calculate_product_rating(review)

        return review
