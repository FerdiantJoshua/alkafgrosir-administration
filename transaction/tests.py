from django.test import TestCase
from django.utils import timezone

from .models import City, Customer, Product, Marketplace, Courier, Transaction, Purchase


class ModelsTest(TestCase):
    def test_model_creation(self):
        city_01 = City.objects.get_or_create(name='BANDUNG')[0]
        city_02 = City.objects.get_or_create(name='JAKARTA')[0]
        customer_01 = Customer.objects.get_or_create(name='Budi', username='budi')[0]
        customer_02 = Customer.objects.get_or_create(name='Anto', username='anto')[0]
        product_01 = Product.objects.get_or_create(code='S1108.HD1674.17', name='HD1674', color='Biru Baby', size='30x70')[0]
        product_02 = Product.objects.get_or_create(code='S1108.HD1674.03', name='HD1674', color='Pink Baby', size='30x70')[0]
        marketplace_01 = Marketplace.objects.get_or_create(name='Shopee', short_name='S')[0]
        marketplace_02 = Marketplace.objects.get_or_create(name='Tokopedia', short_name='T')[0]
        courier_01 = Courier.objects.get_or_create(name='JNE', short_name='JNE')[0]
        courier_02 = Courier.objects.get_or_create(name='JNT', short_name='JNT')[0]

        transaction_01 = Transaction.objects.get_or_create(number=1, date=timezone.now(),
                                  marketplace=marketplace_01, customer=customer_01, city=city_01, courier=courier_01)[0]
        transaction_02 = Transaction.objects.get_or_create(number=2, date=timezone.now(),
                                  marketplace=marketplace_02, customer=customer_02, city=city_02, courier=courier_02)[0]
        purchase_01 = Purchase.objects.get_or_create(transaction=transaction_01, product=product_01, amount=8)[0]
        purchase_02 = Purchase.objects.get_or_create(transaction=transaction_02, product=product_02, amount=10)[0]

        self.assertEqual(transaction_01.purchase_set.get(transaction=transaction_01), purchase_01)
        self.assertEqual(transaction_02.purchase_set.get(transaction=transaction_02), purchase_02)
