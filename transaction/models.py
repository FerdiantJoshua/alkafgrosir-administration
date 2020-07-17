from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse, NoReverseMatch



class City(models.Model):
    name = models.CharField(
        'City Name', max_length=24, unique=True,
        validators=[RegexValidator('^[A-Z \.]*$', 'Only uppercase letters, space, and period are allowed.')]
    )

    def get_absolute_url(self):
        return reverse('management:edit_city', args=[self.pk])

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField('Customer Name', max_length=48)
    username = models.CharField('Username', max_length=48, unique=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('management:edit_customer', args=[self.pk])

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField('Product Code', max_length=64, unique=True)
    name = models.CharField('Product Name', max_length=48)
    color = models.CharField('Product Color', max_length=48)
    size = models.CharField('Product Size', max_length=24)
    stock = models.PositiveIntegerField('Stock', default=0, null=False)

    class Meta:
        unique_together = (('name', 'color', 'size'), )

    def get_absolute_url(self):
        return reverse('management:edit_product', args=[self.pk])

    def __str__(self):
        return f'{self.name} {self.color} {self.size} ({self.code}), {self.stock} remaining'


class Marketplace(models.Model):
    name = models.CharField('Marketplace Name', max_length=24, unique=True)
    short_name = models.CharField('Short Name', max_length=5, unique=True)

    def get_absolute_url(self):
        return reverse('management:edit_marketplace', args=[self.pk])

    def __str__(self):
        return f'{self.short_name} ({self.name})'


class Courier(models.Model):
    name = models.CharField('Marketplace Name', max_length=24, unique=True)
    short_name = models.CharField('Short Name', max_length=5, unique=True)

    def get_absolute_url(self):
        return reverse('management:edit_courier', args=[self.pk])

    def __str__(self):
        return self.name


class TransactionQuerySet(models.QuerySet):
    def search_by_criteria(self, criteria):
        transactions = self.filter(
            Q(date__gte=criteria['date_start']) &
            Q(date__lte=criteria['date_end']) &
            Q(marketplace__name__icontains=criteria.get('marketplace', '')) &
            Q(customer__name__icontains=criteria.get('customer', '')) &
            Q(city__name__icontains=criteria.get('city', '')) &
            Q(purchase__product__code__icontains=criteria.get('purchases', '')) |
            Q(purchase__product__name__icontains=criteria.get('purchases', '')) |
            Q(purchase__product__color__icontains=criteria.get('purchases', '')) |
            Q(purchase__product__size__icontains=criteria.get('purchases', '')) &
            Q(courier__name__icontains=criteria.get('courier', ''))
        ).distinct().order_by('date', 'number')
        if criteria.get('is_prepared'):
            transactions = transactions.filter(is_prepared=criteria['is_prepared'])
        if criteria.get('is_packed'):
            transactions = transactions.filter(is_packed=criteria['is_packed'])

        return transactions


class Transaction(models.Model):
    number = models.PositiveIntegerField('Transaction Number', unique_for_date=True, null=False, editable=False)
    date = models.DateField('Date')
    marketplace = models.ForeignKey(Marketplace, verbose_name='Marketplace', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, verbose_name='City', on_delete=models.SET_NULL, null=True)
    courier = models.ForeignKey(Courier, verbose_name='Courier', on_delete=models.SET_NULL, null=True)
    packager = models.ForeignKey(User, verbose_name='Packager', on_delete=models.SET_NULL, blank=True, null=True)
    is_prepared = models.BooleanField('Is Prepared', default=False)
    is_packed = models.BooleanField('Is Packed', default=False)

    objects = TransactionQuerySet.as_manager()

    @staticmethod
    def get_absolute_attribute_helptext_urls():
        try:
            absolute_attribute_helptext_urls = {
                'marketplace': reverse('management:create_marketplace'),
                'customer': reverse('management:create_customer'),
                'city': reverse('management:create_city'),
                'courier': reverse('management:create_courier')
            }
        except NoReverseMatch as e:
            raise ValueError(f'Problematic get_absolute_attribute_helptext_urls function in {__class__} .') from e
        return absolute_attribute_helptext_urls

    def get_absolute_url(self):
        return reverse('transaction:edit_transaction', args=[self.pk])

    def __str__(self):
        return f'{self.marketplace}-{self.customer.name}-{self.courier}'


class Purchase(models.Model):
    transaction = models.ForeignKey(Transaction, verbose_name='Transaction', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', help_text='Start typing to get product choices',
                                on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField('Amount', default=1, null=False)
    additional_information = models.CharField('Additional Information', max_length=128, blank=True, null=False)

    def __str__(self):
        return f'{self.transaction}-{self.product.name}({self.product.color}) -> {self.amount}' \
                + f' ({self.additional_information})' if {self.additional_information} else ''
