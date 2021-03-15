from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

from store.managers import ProductReviewManager

Customer = get_user_model()


# class CustomerHome(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     # is_active = models.BooleanField(default=True)
#     address = models.CharField(max_length=100)


class ProductsCategory(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)

    class Meta:
        verbose_name = 'Products category'
        verbose_name_plural = 'Products categories'

    def __str__(self):
        return f'{self.slug}'


class ProductsSubcategory(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)

    # relations
    category = models.ForeignKey(ProductsCategory,
                                 related_name='subcategories',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Products subcategory'
        verbose_name_plural = 'Products subcategories'

    def __str__(self):
        return f'{self.slug}'


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # calculated fields
    rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    # relations
    category = models.ForeignKey(ProductsSubcategory,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    customers_who_liked_this = models.ManyToManyField(Customer, related_name='liked_products', blank=True)

    def __str__(self):
        return f'{self.title}'


class ProductPhoto(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='images')

    # relations
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='photos')

    def __str__(self):
        return f'{self.name}'


class ProductReview(models.Model):
    benefits = models.TextField(max_length=500)
    issues = models.TextField(max_length=500)
    comment = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)

    MARK_CHOICES = [(x, x) for x in range(1, 11)]

    mark = models.IntegerField(choices=MARK_CHOICES)

    # relations
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 related_name='reviews')

    objects = ProductReviewManager()

    def __str__(self):
        return f'{self.product.slug}:{self.id}'


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'Cart#{self.id}:{self.customer.username}'


class ProductCartRelation(models.Model):
    count = models.IntegerField(default=1)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,
                             related_name='products',
                             on_delete=models.CASCADE)


class Order(models.Model):
    is_delivery = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # relations
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    class ORDER_STATUS(models.TextChoices):
        WAITING = 'WP', _('Waiting for payment')
        PICKUP = 'OP', _('Order pickup')
        READY = 'RS', _('Ready for self-delivery')
        COMPLETE = 'OC', _('Order complete')

    status = models.CharField(max_length=2,
                              choices=ORDER_STATUS.choices,
                              default=ORDER_STATUS.WAITING)
