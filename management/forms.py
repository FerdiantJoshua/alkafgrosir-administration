from django.forms import ModelForm

from transaction.models import City, Customer, Product, Marketplace, Courier


class CityForm(ModelForm):
    class Meta():
        model = City
        fields = '__all__'



class CustomerForm(ModelForm):
    class Meta():
        model = Customer
        fields = '__all__'



class ProductForm(ModelForm):
    class Meta():
        model = Product
        fields = '__all__'


class MarketplaceForm(ModelForm):
    class Meta():
        model = Marketplace
        fields = '__all__'


class CourierForm(ModelForm):
    class Meta():
        model = Courier
        fields = '__all__'
