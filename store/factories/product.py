from decimal import Decimal
from random import randint, choice

from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory, ImageField

from store.factories.customer import CustomerFactory
from store.models import ProductsCategory, ProductsSubcategory, Product, ProductReview


class ProductsCategoryFactory(DjangoModelFactory):
    class Meta:
        model = ProductsCategory

    title = Sequence(lambda n: f'Category #{n}')
    slug = Sequence(lambda n: f'category #{n}')


class ProductsSubcategoryFactory(DjangoModelFactory):
    class Meta:
        model = ProductsSubcategory

    title = Sequence(lambda n: f'Subcategory #{n}')
    slug = Sequence(lambda n: f'subcategory #{n}')

    category = SubFactory(ProductsCategoryFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    title = Sequence(lambda n: f'Product #{n}')
    slug = Sequence(lambda n: f'product #{n}')
    description = "product's description"
    price = Decimal(f'{randint(0, 999999)}.{randint(0, 99)}')

    category = SubFactory(ProductsSubcategoryFactory)


class ProductReviewFactory(DjangoModelFactory):
    class Meta:
        model = ProductReview

    benefits = 'Benefits'
    issues = 'Issues'
    comment = 'Comment'
    mark = choice(ProductReview.MARK_CHOICES)[0]

    product = SubFactory(ProductFactory)
    customer = SubFactory(CustomerFactory)


class ProductPhoto(DjangoModelFactory):
    name = Sequence(lambda n: f'ProductPhoto #{n}')
    photo = ImageField(color='white')

    product = SubFactory(ProductFactory)





