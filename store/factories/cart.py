from decimal import Decimal

from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from store.factories.customer import CustomerFactory
from store.models import Cart


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    price = Decimal("0.00")
    customer = SubFactory(CustomerFactory)

    @post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.products.add(product)
                self.price += product.price
