from django.test import TestCase
from django.utils import timezone

from .models import City, Customer, Product, Marketplace, Courier, Transaction, Purchase


class ModelsTest(TestCase):
    def test_model_creation(self):
        cities = []
        customers = []
        products = []
        marketplaces = []
        couriers = []
        transactions = []
        purchases = []
        
        cities.append(City.objects.get_or_create(name='BANDUNG')[0])
        cities.append(City.objects.get_or_create(name='JAKARTA')[0])
        cities.append(City.objects.get_or_create(name='SURABAYA')[0])
        customers.append(Customer.objects.get_or_create(name='Budi', username='budi')[0])
        customers.append(Customer.objects.get_or_create(name='Anto', username='anto')[0])
        customers.append(Customer.objects.get_or_create(name='Mawar', username='mawar')[0])
        products.append(Product.objects.get_or_create(code='S1108.HD1674.17', name='HD1674', color='Biru Baby', size='30x70')[0])
        products.append(Product.objects.get_or_create(code='S1108.HD1674.03', name='HD1674', color='Pink Baby', size='30x70')[0])
        products.append(Product.objects.get_or_create(code='S1105.HD122-25', name='HD122', color='Putih', size='30x70')[0])
        marketplaces.append(Marketplace.objects.get_or_create(name='Shopee', short_name='S')[0])
        marketplaces.append(Marketplace.objects.get_or_create(name='Tokopedia', short_name='T')[0])
        marketplaces.append(Marketplace.objects.get_or_create(name='Bukalapak', short_name='BL')[0])
        couriers.append(Courier.objects.get_or_create(name='JNE', short_name='JNE')[0])
        couriers.append(Courier.objects.get_or_create(name='JNT', short_name='JNT')[0])
        couriers.append(Courier.objects.get_or_create(name='SiCepat', short_name='SC')[0])

        transactions.append(Transaction.objects.get_or_create(number=1, date=timezone.now(), marketplace=marketplaces[0], 
                                                            customer=customers[0], city=cities[0], courier=couriers[0])[0])
        transactions.append(Transaction.objects.get_or_create(number=2, date=timezone.now(), marketplace=marketplaces[1],
                                                              customer=customers[1], city=cities[1], courier=couriers[1])[0])
        transactions.append(Transaction.objects.get_or_create(number=2, date=timezone.now(), marketplace=marketplaces[2],
                                                              customer=customers[2], city=cities[2], courier=couriers[2])[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[0], product=products[0], amount=8)[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[1], product=products[1], amount=10)[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[2], product=products[0], amount=12)[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[2], product=products[1], amount=12)[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[2], product=products[2], amount=12)[0])

        self.assertEqual(transactions[0].purchase_set.get(transaction=transactions[0]), purchases[0])
        self.assertEqual(transactions[1].purchase_set.get(transaction=transactions[1]), purchases[1])
        self.assertEqual(len(transactions[2].purchase_set.all()), 3)
