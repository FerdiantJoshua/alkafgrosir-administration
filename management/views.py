from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from transaction.models import City, Customer, Product, Marketplace, Courier
from .forms import CityForm, CustomerForm, ProductForm, MarketplaceForm, CourierForm


class ManagementMainView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'management/main.html'


class MarketplaceCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'management/marketplace_create.html'
    form_class = MarketplaceForm
    success_url = reverse_lazy('management:list_marketplace')


class MarketplaceListView(LoginRequiredMixin, generic.ListView):
    model = Marketplace
    template_name = 'management/marketplace_list.html'
    context_object_name = 'marketplaces'


class MarketplaceEditView(LoginRequiredMixin, generic.FormView, generic.DetailView):
    model = Marketplace
    template_name = 'management/marketplace_edit.html'
    form_class = MarketplaceForm
    success_url = reverse_lazy('management:list_marketplace')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
        form.instance.id = self.object.id
        form.save()
        return super().form_valid(form)


class MarketplaceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Marketplace
    template_name = 'management/marketplace_edit.html'
    success_url = reverse_lazy('management:list_marketplace')


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'management/customer_create.html'
    form_class = CustomerForm
    success_url = reverse_lazy('management:list_customer')


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'management/customer_list.html'
    context_object_name = 'customers'


class CustomerEditView(LoginRequiredMixin, generic.FormView, generic.DetailView):
    model = Customer
    template_name = 'management/customer_edit.html'
    form_class = CustomerForm
    success_url = reverse_lazy('management:list_customer')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
        form.instance.id = self.object.id
        form.save()
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    template_name = 'management/customer_edit.html'
    success_url = reverse_lazy('management:list_customer')


class CityCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'management/city_create.html'
    form_class = CityForm
    success_url = reverse_lazy('management:list_city')


class CityListView(LoginRequiredMixin, generic.ListView):
    model = City
    template_name = 'management/city_list.html'
    context_object_name = 'cities'


class CityEditView(LoginRequiredMixin, generic.FormView, generic.DetailView):
    model = City
    template_name = 'management/city_edit.html'
    form_class = CityForm
    success_url = reverse_lazy('management:list_city')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
        print('puruyeah')
        form.instance.pk = self.object.pk
        form.save()
        return super().form_valid(form)


class CityDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = City
    template_name = 'management/city_edit.html'
    success_url = reverse_lazy('management:list_city')


class CourierCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'management/courier_create.html'
    form_class = CourierForm
    success_url = reverse_lazy('management:list_courier')


class CourierListView(LoginRequiredMixin, generic.ListView):
    model = Courier
    template_name = 'management/courier_list.html'
    context_object_name = 'couriers'


class CourierEditView(LoginRequiredMixin, generic.FormView, generic.DetailView):
    model = Courier
    template_name = 'management/courier_edit.html'
    form_class = CourierForm
    success_url = reverse_lazy('management:list_courier')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
        form.instance.id = self.object.id
        form.save()
        return super().form_valid(form)


class CourierDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Courier
    template_name = 'management/courier_edit.html'
    success_url = reverse_lazy('management:list_courier')


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'management/product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('management:list_product')


class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'management/product_list.html'
    context_object_name = 'products'


class ProductEditView(LoginRequiredMixin, generic.FormView, generic.DetailView):
    model = Product
    template_name = 'management/product_edit.html'
    form_class = ProductForm
    success_url = reverse_lazy('management:list_product')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    template_name = 'management/product_edit.html'
    success_url = reverse_lazy('management:list_product')
