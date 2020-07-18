# Generated by Django 3.0.8 on 2020-07-17 12:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, unique=True, validators=[django.core.validators.RegexValidator('^[A-Z \\.]*$', 'Only uppercase letters, space, and period are allowed.')], verbose_name='City Name')),
            ],
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, verbose_name='Marketplace Name')),
                ('short_name', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='Short Name')),
                ('type', models.CharField(default='Universal', max_length=24, verbose_name='Short Name')),
            ],
            options={
                'unique_together': {('name', 'type')},
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, verbose_name='Customer Name')),
                ('username', models.CharField(blank=True, max_length=48, null=True, unique=True, verbose_name='Username')),
            ],
        ),
        migrations.CreateModel(
            name='Marketplace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True, verbose_name='Marketplace Name')),
                ('short_name', models.CharField(max_length=5, unique=True, verbose_name='Short Name')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True, verbose_name='Product Code')),
                ('name', models.CharField(max_length=48, verbose_name='Product Name')),
                ('color', models.CharField(max_length=48, verbose_name='Product Color')),
                ('size', models.CharField(max_length=24, verbose_name='Product Size')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
            ],
            options={
                'unique_together': {('name', 'color', 'size')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(editable=False, unique_for_date=True, verbose_name='Transaction Number')),
                ('date', models.DateField(verbose_name='Date')),
                ('is_prepared', models.BooleanField(default=False, verbose_name='Is Prepared')),
                ('is_packed', models.BooleanField(default=False, verbose_name='Is Packed')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.City', verbose_name='City')),
                ('courier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.Courier', verbose_name='Courier')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.Customer', verbose_name='Customer')),
                ('marketplace', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.Marketplace', verbose_name='Marketplace')),
                ('packager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Packager')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, verbose_name='Amount')),
                ('product', models.ForeignKey(help_text='Start typing to get product choices', null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.Product', verbose_name='Product')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.Transaction', verbose_name='Transaction')),
                ('additional_information', models.CharField(blank=True, max_length=128, verbose_name='Additional Information')),
            ],
        ),
    ]
