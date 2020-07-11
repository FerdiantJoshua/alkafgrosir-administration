from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from transaction.models import Marketplace
from .forms import MarketplaceForm


class ManagementMainView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'management/main.html'


class MarketplaceCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'management/marketplace_create.html'
    form_class = MarketplaceForm
    success_url = reverse_lazy('management:list_marketplace')


class MarketplaceListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    model = Marketplace
    template_name = 'management/marketplace_list.html'
    context_object_name = 'marketplaces'


class MarketplaceView(LoginRequiredMixin, generic.FormView, generic.DetailView):
    model = Marketplace
    template_name = 'management/marketplace_view.html'
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
    template_name = 'management/lesson_view.html'
    success_url = reverse_lazy('management:list_marketplace')
