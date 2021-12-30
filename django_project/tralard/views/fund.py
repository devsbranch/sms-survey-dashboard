from re import template
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.models.fund import Fund, FundDisbursed, FundExpenditure


class FundListView(LoginRequiredMixin, generic.ListView):
    model = Fund
    context_object_name = 'funds'
    template_name = 'fund/list.html'
    
    def get_context_data(self):
        context = super(FundListView, self).get_context_data()
        context['title'] = 'Funds'
        return context

class FundDetailView(LoginRequiredMixin, generic.DetailView):
    model = Fund
    context_object_name = 'fund'
    template_name = 'fund/detail.html'
    
    def get_context_data(self):
        context = super(FundDetailView, self).get_context_data()
        context['title'] = 'Funds'
        return context
