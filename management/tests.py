from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from alkaf_administration.settings import LOGIN_URL
from transaction.models import Marketplace
from .urls import app_name, urlpatterns


class AnonymousAccessTest(TestCase):
    def test_deny_anonymous(self):
        require_pk = ['edit', 'delete']
        default_pk = 1
        urls = list(map(lambda x: x.name, urlpatterns))
        for url in urls:
            complete_url = f'{app_name}:{url}'
            url = reverse(complete_url, args=[default_pk]) if url.split('_')[0] in require_pk else reverse(complete_url)
            response = self.client.get(url, follow=True)
            self.assertRedirects(response, f'{reverse(LOGIN_URL)}?next={url}')


class MarketplaceViewTest(TestCase):
    username = 'username'
    password = 'password'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        User.objects.create_superuser(
            username=MarketplaceViewTest.username, password=MarketplaceViewTest.password
        )

    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)

    def test_createview(self):
        url = reverse('management:create_marketplace')
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

        data = {'name': 'Tokopedia', 'short_name': 'T'}
        marketplace = Marketplace(name=data['name'], short_name=data['short_name'])
        self.client.post(url, data)
        saved_marketplace = Marketplace.objects.get(short_name='T')
        self.assertEqual(saved_marketplace.name, marketplace.name)
        self.assertEqual(saved_marketplace.short_name, marketplace.short_name)

