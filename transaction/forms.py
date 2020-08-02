from django import forms
from django.core.exceptions import ValidationError
from django.forms import Select
from django.utils.translation import gettext as _

from alkaf_administration.settings import DATETIME_FORMAT
from .models import Transaction, Purchase


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = [DATETIME_FORMAT]

    class Meta():
        model = Transaction
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(format=DATETIME_FORMAT),
            'customer': forms.TextInput(attrs={'class': 'has-autocomplete'}),
            'city': forms.TextInput(attrs={'class': 'has-autocomplete'})
        }
        help_texts = {
            'marketplace': 'Add marketplace',
            'customer': 'Add customer',
            'city': 'Add city',
            'courier': 'Add courier',
        }


class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['amount'].initial = ''

    def clean(self):
        print('purchaseform cleaned_data:', self.cleaned_data)
        previous_amount = 0
        if self.instance:
            print('purchase\'s instance amount (cleaning process):', self.instance.amount)
            previous_amount = self.instance.amount
        if (self.cleaned_data.get('amount') and self.cleaned_data.get('product')) and \
            self.cleaned_data['amount'] - previous_amount > self.cleaned_data['product'].stock:
            error_msg = 'The amount of this product purchase is greater than the remaining stock!'
            raise ValidationError({'amount': error_msg})
        return self.cleaned_data

    class Meta():
        model = Purchase
        fields = '__all__'
        widgets = {
            'product': forms.TextInput(attrs={'class': 'has-autocomplete'})
        }


PurchaseFormSet = forms.inlineformset_factory(
    Transaction,
    Purchase,
    form=PurchaseForm,
    extra=0,
    min_num=1,
)


class CustomNullBooleanSelect(forms.NullBooleanSelect):
    def __init__(self, choices, attrs=None):
        choices = choices or (
            ('unknown', _('Unknown')),
            ('true', _('Yes')),
            ('false', _('No')),
        )
        Select.__init__(self, attrs, choices)


class TransactionSearchForm(forms.Form):
    IS_PREPARED_CHOICES = (
        (None, _('-----Is Prepared?-----')),
        (True, _('Yes')),
        (False, _('No')),
    )
    IS_PACKED_CHOICES = (
        (None, _('-----Is Packed?-----')),
        (True, _('Yes')),
        (False, _('No')),
    )

    date_start = forms.DateField(required=False, input_formats=[DATETIME_FORMAT],
                                 widget=forms.DateInput(format=DATETIME_FORMAT))
    date_end = forms.DateField(required=False, input_formats=[DATETIME_FORMAT],
                               widget=forms.DateInput(format=DATETIME_FORMAT))
    marketplace = forms.CharField(required=False)
    customer = forms.CharField(required=False)
    city = forms.CharField(required=False)
    purchases = forms.CharField(required=False)
    courier = forms.CharField(required=False)
    packager = forms.CharField(required=False, help_text='Type \'None\' for no packager')
    is_prepared = forms.NullBooleanField(label='', required=False, widget=CustomNullBooleanSelect(choices=IS_PREPARED_CHOICES))
    is_packed = forms.NullBooleanField(label='', required=False, widget=CustomNullBooleanSelect(choices=IS_PACKED_CHOICES))


class TransactionDuplicationForm(forms.Form):
    def __init__(self, type='search', *args, **kwargs):
        super(TransactionDuplicationForm, self).__init__(*args, **kwargs)
        if type != 'search':
            for field_name in self.fields:
                if field_name not in ['times', 'omit_purchases']:
                    self.fields[field_name].widget.input_type = 'hidden'
                    self.fields[field_name].required = False
        else:
            self.fields['times'].widget.input_type = 'hidden'
            self.fields['omit_purchases'].widget.input_type = 'hidden'

    def clean(self):
        transaction = Transaction.objects.get(date=self.cleaned_data['date'], number=self.cleaned_data['number'])
        if not self.cleaned_data['omit_purchases']:
            for purchase in transaction.purchase_set.all():
                if self.cleaned_data['times'] * purchase.amount > purchase.product.stock:
                    error_msg = f'The amount of product {purchase.product.name} {purchase.product.color} purchase will \
                                be greater than the remaining stock if multiplied {self.cleaned_data["times"]} times!'
                    raise ValidationError({'times': error_msg})
        return self.cleaned_data

    date = forms.DateField(input_formats=[DATETIME_FORMAT],
                                 widget=forms.DateInput(format=DATETIME_FORMAT))
    number = forms.IntegerField(min_value=1)
    times = forms.IntegerField(initial=1, min_value=1, max_value=5,
                               help_text='Duplicate the transaction this many times. Maximum 5 duplication at a time.')
    omit_purchases = forms.BooleanField(required=False,
        help_text='Duplicate the transaction without the purchases.'
    )
