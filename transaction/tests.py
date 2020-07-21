from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from alkaf_administration.settings import LOGIN_URL
from .models import City, Customer, Product, Marketplace, Courier, Transaction, Purchase
from .urls import app_name, urlpatterns


class AnonymousAccessTest(TestCase):
    def test_deny_anonymous(self):
        default_pk = 1
        require_pk = ['edit', 'delete']
        urls = list(map(lambda x: x.name, urlpatterns))
        for url in urls:
            complete_url = f'{app_name}:{url}'
            url = reverse(complete_url, args=[default_pk]) if url.split('_')[0] in require_pk else reverse(complete_url)
            response = self.client.get(url, follow=True)
            self.assertRedirects(response, f'{reverse(LOGIN_URL)}?next={url}')


class TransactionAppTest(TestCase):
    username = 'username'
    password = 'password'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        User.objects.create_superuser(
            username=TransactionAppTest.username, password=TransactionAppTest.password
        )

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
        products.append(
            Product.objects.get_or_create(code='S1108.HD1674.17', name='HD1674', color='Biru Baby', size='30x70',
                                          stock=100)[0])
        products.append(
            Product.objects.get_or_create(code='S1108.HD1674.03', name='HD1674', color='Pink Baby', size='30x70',
                                          stock=100)[0])
        products.append(
            Product.objects.get_or_create(code='S1105.HD122-25', name='HD122', color='Putih', size='30x70', stock=100)[
                0])
        marketplaces.append(Marketplace.objects.get_or_create(name='Shopee', short_name='S')[0])
        marketplaces.append(Marketplace.objects.get_or_create(name='Tokopedia', short_name='T')[0])
        marketplaces.append(Marketplace.objects.get_or_create(name='Bukalapak', short_name='BL')[0])
        couriers.append(Courier.objects.get_or_create(name='JNE', type='OK', short_name='JNE')[0])
        couriers.append(Courier.objects.get_or_create(name='JNT', short_name='JNT')[0])
        couriers.append(Courier.objects.get_or_create(name='SiCepat', short_name='SC')[0])

        transactions.append(
            Transaction.objects.get_or_create(number=1, date=timezone.now(), marketplace=marketplaces[0],
                                              customer=customers[0], city=cities[0], courier=couriers[0])[0])
        transactions.append(
            Transaction.objects.get_or_create(number=2, date=timezone.now(), marketplace=marketplaces[1],
                                              customer=customers[1], city=cities[1], courier=couriers[1])[0])
        transactions.append(
            Transaction.objects.get_or_create(number=3, date=timezone.now(), marketplace=marketplaces[2],
                                              customer=customers[2], city=cities[2], courier=couriers[2])[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[0], product=products[0], amount=8)[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[1], product=products[1], amount=10)[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[2], product=products[0], amount=12)[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[2], product=products[1], amount=12)[0])
        purchases.append(Purchase.objects.get_or_create(transaction=transactions[2], product=products[2], amount=12)[0])

    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.first_transaction = Transaction.objects.first()

    def test_get_list_transaction(self):
        url = reverse('transaction:list_transaction')

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

    def test_get_create_transaction(self):
        url = reverse('transaction:create_transaction')

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

    def test_get_edit_transaction(self):
        url = reverse('transaction:edit_transaction', args=[self.first_transaction.pk])

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

    def test_get_delete_transaction(self):
        url = reverse('transaction:delete_transaction', args=[self.first_transaction.pk])

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

    def test_get_duplicate_transaction(self):
        url = reverse('transaction:duplicate_transaction')

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
