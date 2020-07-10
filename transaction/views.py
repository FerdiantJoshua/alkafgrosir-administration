from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import TransactionForm, PurchaseFormSet


class MainTransactionView(LoginRequiredMixin, generic.FormView):
    template_name = 'transaction/main_transaction.html'
    form_class = TransactionForm
    success_url = reverse_lazy('transaction:index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.purchase_formset = self.get_context_data()['purchase_formset']
        if form.is_valid() and self.purchase_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['purchase_formset'] = PurchaseFormSet(self.request.POST)
        else:
            context['purchase_formset'] = PurchaseFormSet()
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.purchase_formset.instance = self.object
        self.purchase_formset.save()
        return super().form_valid(form)
