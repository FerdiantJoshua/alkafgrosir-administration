from django.forms import ModelForm, inlineformset_factory

from .models import Transaction, Purchase


class TransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        date_format = ['%Y/%m/%d']
        self.fields['date'].input_formats = date_format

    class Meta():
        model = Transaction
        fields = '__all__'


class PurchaseForm(ModelForm):
    class Meta():
        model = Purchase
        fields = '__all__'


PurchaseFormSet = inlineformset_factory(
    Transaction,
    Purchase,
    form=PurchaseForm,
    extra=1,
    min_num=1,
)
