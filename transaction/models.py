from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(
        'City Name', max_length=24,
        primary_key=True, unique=True,
        validators=[RegexValidator('^[A-Z_]*$', 'Only uppercase letters and underscores allowed.')]
    )

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField('Customer Name', max_length=48)
    username = models.CharField('Username', max_length=48, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField('Product Code', max_length=64, unique=True, primary_key=True)
    name = models.CharField('Product Name', max_length=48)
    color = models.CharField('Product Color', max_length=48)
    size = models.CharField('Product Size', max_length=24)
    stock = models.PositiveIntegerField('Stock', default=0, null=False)

    class Meta:
        unique_together = (('name', 'color', 'size'), )

    def __str__(self):
        return f'{self.code} ({self.name}-{self.size}-{self.color}) = {self.stock}'


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

    def __str__(self):
        return self.name


class Transaction(models.Model):
    number = models.PositiveIntegerField('Transaction Number', unique_for_date=True, null=False, editable=False)
    date = models.DateField('Date')
    marketplace = models.ForeignKey(Marketplace, verbose_name='Marketplace', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, verbose_name='City', on_delete=models.SET_NULL, null=True)
    courier = models.ForeignKey(Courier, verbose_name='Courier', on_delete=models.SET_NULL, null=True)
    is_prepared = models.BooleanField('Is Prepared', default=False)
    is_packed = models.BooleanField('Is Packed', default=False)

    def get_absolute_url(self):
        return reverse('transaction:edit_transaction', args=[self.pk])

    def __str__(self):
        return f'{self.marketplace}-{self.customer.name}-{self.courier}'


class Purchase(models.Model):
    transaction = models.ForeignKey(Transaction, verbose_name='Transaction', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', help_text='Start typing to get product choices',
                                on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField('Amount', default=1, null=False)

    def __str__(self):
        return f'{self.transaction}-{self.product.name}({self.product.color}) -> {self.amount}'
