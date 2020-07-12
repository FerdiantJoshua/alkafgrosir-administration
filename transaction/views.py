import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.db.models.base import ModelBase
from django.urls import reverse_lazy
from django.views import generic

from .forms import TransactionForm, PurchaseFormSet
from .models import Transaction, Product, City


class TransactionListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 3
    model = Transaction
    template_name = 'transaction/transaction_list.html'
    context_object_name = 'transactions'
    ordering = 'date'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        fields = self.object_list.first()._meta.fields
        current_page = self.request.GET.get(self.page_kwarg) or 1
        request_params = re.sub(r'&page=[0-9]*', '', self.request.get_full_path().split('/')[-1])
        context['fields'] = fields
        context['current_page'] = int(current_page)
        context['request_params'] = '?' + request_params if '?' not in request_params else request_params
        return context


def _get_list_of_available_record(model_base: ModelBase):
    return list(map(lambda x: {'value': x.pk, 'label': str(x)}, model_base.objects.all()))


class TransactionCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'transaction/transaction_create.html'
    form_class = TransactionForm
    success_url = reverse_lazy('transaction:list_transaction')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.purchase_formset = self.get_context_data()['formset']
        if form.is_valid() and self.purchase_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PurchaseFormSet(self.request.POST)
        else:
            context['formset'] = PurchaseFormSet()
        context['available_product'] = json.dumps(_get_list_of_available_record(Product))
        context['available_city'] = json.dumps(_get_list_of_available_record(City))
        return context

    def form_valid(self, form):
        prev_number = Transaction.objects.filter(date=form.instance.date).aggregate(Max('number'))['number__max']
        print(prev_number)
        form.instance.number = prev_number + 1 if prev_number else 1
        self.object = form.save()
        self.purchase_formset.instance = self.object
        self.purchase_formset.save()
        return super().form_valid(form)


class TransactionEditView(LoginRequiredMixin, generic.FormView, generic.DetailView):
    model = Transaction
    template_name = 'transaction/transaction_edit.html'
    form_class = TransactionForm
    success_url = reverse_lazy('transaction:list_transaction')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.purchase_formset = self.get_context_data()['formset']
        if form.is_valid() and self.purchase_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PurchaseFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = PurchaseFormSet(instance=self.object)
        print(context['formset'])
        context['available_product'] = json.dumps(_get_list_of_available_record(Product))
        context['available_city'] = json.dumps(_get_list_of_available_record(City))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
        form.instance.id = self.object.id
        self.purchase_formset.instance = self.object
        form.save()
        self.purchase_formset.save()
        return super().form_valid(form)


class TransactionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Transaction
    template_name = 'transaction/transaction_edit.html'
    success_url = reverse_lazy('transaction:list_transaction')
