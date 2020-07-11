from django.forms import ModelForm

from transaction.models import Marketplace


class MarketplaceForm(ModelForm):
    class Meta():
        model = Marketplace
        fields = '__all__'
