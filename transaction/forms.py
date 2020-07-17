from django import forms
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
    is_prepared = forms.NullBooleanField(label='', required=False, widget=CustomNullBooleanSelect(choices=IS_PREPARED_CHOICES))
    is_packed = forms.NullBooleanField(label='', required=False, widget=CustomNullBooleanSelect(choices=IS_PACKED_CHOICES))
    marketplace = forms.CharField(required=False)
    customer = forms.CharField(required=False)
    city = forms.CharField(required=False)
    purchases = forms.CharField(required=False)
    courier = forms.CharField(required=False)
