# Generated by Django 3.0.8 on 2020-07-21 12:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='receipt_number',
            field=models.CharField(blank=True, help_text='Only uppercase letters, and numbers are allowed.', max_length=64, validators=[django.core.validators.RegexValidator('^[A-Z0-9]*$', 'Only uppercase letters, and numbers are allowed.')], verbose_name='Receipt Number'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='shipping_cost',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Shipping Cost'),
        ),
    ]