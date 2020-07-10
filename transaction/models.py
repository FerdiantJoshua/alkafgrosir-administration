from django.db import models


class City(models.Model):
    name = models.CharField('City Name', max_length=24)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField('Customer Name', max_length=48)
    username = models.CharField('Username', max_length=48, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField('Color Name', max_length=24, unique=True)
    short_name = models.CharField('Short Name', max_length=5, unique=True)

    def __str__(self):
        return f'{self.short_name}({self.name})'


class Product(models.Model):
    name = models.CharField('Product Name', max_length=48, unique=True)

    def __str__(self):
        return self.name


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='Color', on_delete=models.CASCADE)
    stock = models.IntegerField('Stock', default=0, null=False)

    class Meta:
        unique_together = (('product', 'color'), )

    def __str__(self):
        return f'{self.product}-{self.color}-{self.stock}'


class Marketplace(models.Model):
    name = models.CharField('Marketplace Name', max_length=24, unique=True)
    short_name = models.CharField('Short Name', max_length=5, unique=True)

    def __str__(self):
        return f'{self.short_name} ({self.name})'


class Courier(models.Model):
    name = models.CharField('Marketplace Name', max_length=24, unique=True)
    short_name = models.CharField('Short Name', max_length=5, unique=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField('Date')
    marketplace = models.ForeignKey(Marketplace, verbose_name='Marketplace', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, verbose_name='City', on_delete=models.SET_NULL, null=True)
    courier = models.ForeignKey(Courier, verbose_name='Courier', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.marketplace}-{self.customer.name}-{self.courier}'


class Purchase(models.Model):
    transaction = models.ForeignKey(Transaction, verbose_name='Transaction', on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation, verbose_name='Product Variation',
                                          on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField('Amount', default=1, null=False)

    def __str__(self):
        return f'{self.transaction}-{self.product_variation.product}({self.product_variation.color}) -> {self.amount}'
