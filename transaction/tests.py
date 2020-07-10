from django.test import TestCase
from django.utils import timezone

from .models import City, Customer, Color, Product, ProductVariation, Marketplace, Courier, Transaction, Purchase


class ModelsTest(TestCase):
    def test_model_creation(self):
        city = City.objects.get_or_create(name='Bandung')[0]
        customer = Customer.objects.get_or_create(name='Budi', username='si_budi')[0]
        color = Color.objects.get_or_create(name='Biru Baby', short_name='BB')[0]
        product = Product.objects.get_or_create(name='HD1674')[0]
        product_variation = ProductVariation.objects.get_or_create(product=product, color=color)[0]
        marketplace = Marketplace.objects.get_or_create(name='Shopee', short_name='S')[0]
        courier = Courier.objects.get_or_create(name='JnE', short_name='JnE')[0]
        transaction = Transaction.objects.get_or_create(date=timezone.now(),
                                  marketplace=marketplace, customer=customer, city=city, courier=courier)[0]
        purchase = Purchase.objects.get_or_create(transaction=transaction, product_variation=product_variation)[0]
        self.assertEqual(transaction.purchase_set.get(transaction=transaction), purchase)
