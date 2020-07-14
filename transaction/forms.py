from django import forms

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
            'city': forms.TextInput()
        }


class PurchaseForm(forms.ModelForm):
    class Meta():
        model = Purchase
        fields = '__all__'
        widgets = {
            'product': forms.TextInput()
        }


PurchaseFormSet = forms.inlineformset_factory(
    Transaction,
    Purchase,
    form=PurchaseForm,
    extra=0,
    min_num=1,
)


class TransactionSearchForm(forms.Form):
    date_start = forms.DateField(required=False,
                                 widget=forms.DateInput(format=DATETIME_FORMAT), input_formats=[DATETIME_FORMAT])
    date_end = forms.DateField(required=False,
                               widget=forms.DateInput(format=DATETIME_FORMAT), input_formats=[DATETIME_FORMAT])
    marketplace = forms.CharField(required=False)
    customer = forms.CharField(required=False)
    city = forms.CharField(required=False)
    purchases = forms.CharField(required=False)
    courier = forms.CharField(required=False)
    is_prepared = forms.BooleanField(required=False)
    is_packed = forms.BooleanField(required=False)
