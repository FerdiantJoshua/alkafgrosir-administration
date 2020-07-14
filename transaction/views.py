import json
import re
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.db.models.base import ModelBase
from django.urls import reverse_lazy
from django.views import generic

from alkaf_administration.settings import DATETIME_FORMAT
from .forms import TransactionForm, PurchaseFormSet, TransactionSearchForm
from .models import Transaction, Product, City


class TransactionListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 3
    model = Transaction
    template_name = 'transaction/transaction_list.html'
    context_object_name = 'transactions'
    ordering = 'date'

    def _retrieve_default_get_params(self):
        params = dict(self.request.GET)
        for key in params:
            params[key] = params[key][0]
        today_date = datetime.today()
        params['date_start'] = datetime.strptime(params['date_start'], DATETIME_FORMAT) if params.get('date_start')\
            else today_date
        params['date_end'] = datetime.strptime(params['date_end'], DATETIME_FORMAT) if params.get('date_end')\
            else today_date
        return params

    def get_queryset(self):
        params = self._retrieve_default_get_params()
        transactions = Transaction.objects.filter(
            date__gte=params['date_start'],
            date__lte=params['date_end'],
            marketplace__name__icontains=params.get('marketplace', ''),
            customer__name__icontains=params.get('customer', ''),
            city__name__icontains=params.get('city', ''),
            purchase__product__name__icontains=params.get('purchase', ''),
            courier__name__icontains=params.get('courier', ''),
        ).distinct()

        return transactions

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if 'form_search' not in kwargs:
            context['form_search'] = TransactionSearchForm(initial=self._retrieve_default_get_params())

        current_page = self.request.GET.get(self.page_kwarg) or 1
        request_params = re.sub(r'&page=[0-9]*', '', self.request.get_full_path().split('/')[-1])

        context['current_page'] = int(current_page)
        context['request_params'] = '?' + request_params if '?' not in request_params else request_params
        return context


def _get_list_of_available_record(model_base: ModelBase):
    return list(map(lambda x: {'value': x.pk, 'label': str(x)}, model_base.objects.all()))


class TransactionCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'transaction/transaction_create.html'
    form_class = TransactionForm
    success_url = reverse_lazy('transaction:list_transaction')
    initial = {'date': datetime.today()}

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
        context['available_product'] = _get_list_of_available_record(Product)
        context['available_city'] = _get_list_of_available_record(City)
        return context

    def form_valid(self, form):
        prev_number = Transaction.objects.filter(date=form.instance.date).aggregate(Max('number'))['number__max']
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
        context['available_product'] = _get_list_of_available_record(Product)
        context['available_city'] = _get_list_of_available_record(City)
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
