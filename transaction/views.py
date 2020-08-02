import csv
import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction as django_transaction
from django.db.models import Max
from django.db.models.base import ModelBase
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.http import require_http_methods

from alkaf_administration.settings import DATETIME_FORMAT
from .forms import TransactionForm, PurchaseFormSet, TransactionSearchForm, TransactionDuplicationForm
from .models import Transaction, Product, City, Customer


def retrieve_default_get_params(get_request):
    params = dict(get_request)
    for key in params:
        params[key] = params[key][0]
    params['date_start'] = get_date_in_safe_format(params.get('date_start'))
    params['date_end'] = get_date_in_safe_format(params.get('date_end'))
    return params


def get_date_in_safe_format(string_date, datetime_format=DATETIME_FORMAT, default=None, supress_error=True):
    if isinstance(string_date, datetime):
        return string_date
    # Default date setting is done in function level to make sure datetime.today() always updates
    default = datetime.today() if default is None else default
    string_date = string_date or ''
    try:
        date = datetime.strptime(string_date, datetime_format)
    except ValueError as e:
        if not supress_error:
            print(e)
            print('Returning default value:', default)
        date = default
    return date


def _get_list_of_available_record(model_base: ModelBase):
    def abbreviate(text, full_single_word=False):
        stripped = text.strip().lower()
        splitted = stripped.split()
        if len(splitted) > 1:
            return ''.join(list(map(lambda x: x[0], splitted)))
        elif not full_single_word:
            return stripped[:3]
        else:
            return stripped

    if model_base is Product:
        return list(map(
            lambda x: {'value': x.pk, 'label': str(x), 'name': abbreviate(x.name, True), 'color': abbreviate(x.color)},
            model_base.objects.all()
        ))
    else:
        return list(map(lambda x: {'value': x.pk, 'label': str(x)}, model_base.objects.all()))


class TransactionListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 20
    model = Transaction
    template_name = 'transaction/transaction_list.html'
    context_object_name = 'transactions'
    ordering = 'date'

    def get_queryset(self):
        params = retrieve_default_get_params(self.request.GET)
        return Transaction.objects.search_by_criteria(params)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if 'form_search' not in kwargs:
            search_form = TransactionSearchForm(initial=retrieve_default_get_params(self.request.GET))
            context['form_search'] = search_form

        request_params = re.sub(r'&page=[0-9]*', '', self.request.get_full_path().split('/')[-1])
        context['request_params'] = '?' + request_params if '?' not in request_params else request_params
        return context


@require_http_methods(['GET'])
@login_required
def export_transaction(request):
    def _render_purchase_querysets(purchase_querysets):
        output = []
        for purchase in purchase_querysets:
            purchase_text = f'{purchase.product.name} ({purchase.product.color}) = {purchase.amount}'
            purchase_text += f' ({purchase.additional_information})' if purchase.additional_information else ''
            output.append(purchase_text)
        return ';'.join(output)

    if request.method == 'GET':
        params = retrieve_default_get_params(request.GET)
        transactions = Transaction.objects.search_by_criteria(params)
        if transactions:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            output = []
            for transaction in transactions:
                purchases = _render_purchase_querysets(transaction.purchase_set.all())
                output.append(list(map(lambda x: str(x).replace(',', ';'), [
                    transaction.date, transaction.number, transaction.marketplace, transaction.customer,
                    transaction.city, purchases, transaction.courier, transaction.receipt_number,
                    transaction.shipping_cost
                ])))
            writer.writerow(['date_start', '#', 'marketplace', 'customer', 'city', 'purchases', 'courier',
                              'receipt_number', 'shipping_cost'])
            writer.writerows(output)

            filename = 'transaction'
            for key, value in params.items():
                if value:
                    value = str(value).split()[0] if 'date' in key else value
                    filename += f'_{key}-{value}'.replace(' ', ',')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

            return response
        else:
            message = 'Unable to export, no transaction is found with those criteria!'
            messages.error(request, message)
            url = request.META.get('HTTP_REFERER') or reverse('transaction:list_transaction')
            return HttpResponseRedirect(url)


@require_http_methods(['GET'])
@login_required
def update_status_is_packed(request):
    if request.method == 'GET':
        params = retrieve_default_get_params(request.GET)
        transactions = Transaction.objects.search_by_criteria(params)
        if transactions:
            message = f'Is_prepared and Is_packed status successfuly updated! \
                        (affects {transactions.count()} transactions)'
            messages.success(request, message)
            transactions.update(is_prepared=True, is_packed=True)
        else:
            message = 'Unable to change status, no transaction is found with those criteria!'
            messages.error(request, message)
        url = request.META.get('HTTP_REFERER') or reverse('transaction:list_transaction')
        return HttpResponseRedirect(url)


class TransactionCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'transaction/transaction_create.html'
    form_class = TransactionForm
    success_url = reverse_lazy('transaction:list_transaction')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'date': datetime.today(), 'packager': self.request.user})
        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        purchase_formset = self.get_context_data()['formset']
        return self._handle_form_and_formset(form, purchase_formset)

    def _handle_form_and_formset(self, form, formset):
        if form.is_valid() and formset.is_valid():
            return self.form_and_formset_valid(form, formset)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['formset'] = PurchaseFormSet(self.request.POST, instance=kwargs.get('formset_instance'))
        else:
            context['formset'] = PurchaseFormSet(instance=kwargs.get('formset_instance'))
        context['available_city'] = _get_list_of_available_record(City)
        context['available_customer'] = _get_list_of_available_record(Customer)
        context['available_product'] = _get_list_of_available_record(Product)
        context['attribute_helptext_urls'] = context['form']._meta.model.get_absolute_attribute_helptext_urls()
        return context

    def form_and_formset_valid(self, form, formset):
        formset.instance = form.instance
        with django_transaction.atomic():
            form.save()
            formset.save()
        messages.success(self.request, _('Transaction creation success!'))
        return self.form_valid(form)


def _extract_path_param_value_as_str(full_path, first_param_name):
    get_params = ''
    splitted_path = full_path.split(f'?{first_param_name}=')
    if len(splitted_path) == 2:
        get_params = splitted_path[-1]
    return get_params


class TransactionEditView(TransactionCreateView, generic.DetailView):
    model = Transaction
    template_name = 'transaction/transaction_edit.html'
    form_class = TransactionForm
    success_url = reverse_lazy('transaction:list_transaction')

    def get_success_url(self):
        success_url = super().get_success_url()
        next_page_url = _extract_path_param_value_as_str(self.request.get_full_path(), 'next')
        return success_url if not next_page_url else next_page_url

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(formset_instance=self.object, **kwargs)
        splitted_path = self.request.get_full_path().split('?', 1)
        context['next_page_url_params'] = '?' + splitted_path[-1] if len(splitted_path) == 2 else ''
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        if kwargs['instance'].date:
            del kwargs['initial']['date']
        return kwargs

    def form_and_formset_valid(self, form, formset):
        form.instance.id = self.object.id
        formset.instance = self.object
        with django_transaction.atomic():
            form.save()
            formset.save()
        messages.success(self.request, _('Transaction edit success!'))
        return self.form_valid(form)


class TransactionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Transaction
    template_name = 'transaction/transaction_edit.html'
    success_url = reverse_lazy('transaction:list_transaction')

    def get_success_url(self):
        success_url = super().get_success_url()
        next_page_url = _extract_path_param_value_as_str(self.request.get_full_path(), 'next')
        return success_url if not next_page_url else next_page_url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        for purchase in self.object.purchase_set.all():
            purchase.delete()
        self.object.delete()
        messages.success(self.request, _('Transaction deletion success!'))
        return HttpResponseRedirect(self.get_success_url())


class TransactionDuplicateView(LoginRequiredMixin, generic.FormView):
    template_name = 'transaction/transaction_duplicate.html'
    success_url = reverse_lazy('transaction:list_transaction')
    form_class = TransactionDuplicationForm
    initial = {
        'date': datetime.today(),
        'number': Transaction.objects.filter(date=datetime.today()).aggregate(Max('number'))['number__max']
    }

    DUP_MARKER_REGEX = re.compile(r'((?:\d)+)-th order')

    def post(self, request, *args, **kwargs):
        submission_form_kwargs = {'type': 'submission'}
        submission_form_kwargs.update(self.get_form_kwargs())
        form_submission = self.form_class(**submission_form_kwargs)
        if form_submission.is_valid():
            return self.form_valid(form_submission)
        else:
            return self.form_invalid(form_submission)

    def get_initial(self):
        initial = super().get_initial()
        for key in self.request.GET:
            if key == 'date':
                initial[key] = get_date_in_safe_format(self.request.GET[key]) if key == 'date' else initial.get(key)
            else:
                initial[key] = self.request.GET[key]
        print(initial)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        transaction = Transaction.objects.filter(
            date=form.initial['date'], number=form.initial['number']
        ).first()
        context['transaction'] = transaction
        if transaction and 'form_submission' not in kwargs:
            submission_form_kwargs = {'type': 'submission'}
            submission_form_kwargs.update(self.get_form_kwargs())
            form_submission = self.form_class(**submission_form_kwargs)
            context['form_submission'] = form_submission
        return context

    def form_valid(self, form):
        date = get_date_in_safe_format(form.data['date'])
        number = int(form.data['number'])
        times = int(form.data['times'])
        max_number_in_date = Transaction.objects.filter(date=date).aggregate(Max('number'))['number__max']
        transaction = Transaction.objects.get(date=date, number=number)
        purchases = transaction.purchase_set.all()
        with django_transaction.atomic():
            for i in range(1, times + 1):
                transaction.id = None
                transaction.number = number + i
                new_transaction = Transaction.objects.create(
                    number=max_number_in_date+i, date=transaction.date, marketplace=transaction.marketplace,
                    customer=transaction.customer, city=transaction.city, courier=transaction.courier,
                    packager=transaction.packager, is_prepared=transaction.is_prepared, is_packed=transaction.is_packed
                )

                if not form.data.get('omit_purchases'):
                    for purchase in purchases:
                        purchase.id = None
                        purchase.transaction = new_transaction
                        purchase_dup_info = re.search(self.DUP_MARKER_REGEX, purchase.additional_information)
                        if purchase_dup_info:
                            purchase.additional_information = re.sub(
                                self.DUP_MARKER_REGEX,
                                f'{int(purchase_dup_info.groups()[0])+1}-th order', purchase.additional_information
                            )
                        else:
                            purchase.additional_information += f'{i+1}-th order' if not purchase.additional_information\
                                                                else f' ({i+1}-th order)'
                        purchase.save()
        messages.success(self.request, _('Transaction duplication success!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form_submission=form))
