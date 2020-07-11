from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from transaction.models import Marketplace


class MarketplaceViewTest(TestCase):
    username = 'username'
    password = 'password'
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_superuser(
            username=MarketplaceViewTest.username, password=MarketplaceViewTest.password
        )

    def test_createview_deny_anonymous(self):
        url = reverse('management:create_marketplace')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'{reverse("account:login")}?next={url}')
        response = self.client.post(reverse('management:create_marketplace'), follow=True)
        self.assertRedirects(response, f'{reverse("account:login")}?next={url}')

    def test_createview(self):
        url = reverse('management:create_marketplace')
        self.client.login(username=self.username, password=self.password)

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

        data = {'name': 'Tokopedia', 'short_name': 'T'}
        marketplace = Marketplace(name=data['name'], short_name=data['short_name'])
        self.client.post(url, data)
        saved_marketplace = Marketplace.objects.get(short_name='T')
        self.assertEqual(saved_marketplace.name, marketplace.name)
        self.assertEqual(saved_marketplace.short_name, marketplace.short_name)

