from django.forms import ModelForm, inlineformset_factory, TextInput

from .models import Transaction, Purchase


class TransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        date_format = ['%d-%m-%Y']
        self.fields['date'].input_formats = date_format

    class Meta():
        model = Transaction
        fields = '__all__'
        widgets = {
            'city': TextInput()
        }


class PurchaseForm(ModelForm):
    class Meta():
        model = Purchase
        fields = '__all__'
        widgets = {
            'product': TextInput()
        }


PurchaseFormSet = inlineformset_factory(
    Transaction,
    Purchase,
    form=PurchaseForm,
    extra=0,
    min_num=1,
)
