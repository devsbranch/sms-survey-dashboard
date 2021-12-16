from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class BeneficiaryOrgListView(LoginRequiredMixin, TemplateView):
    template_name = 'beneficiary/list.html'
    
    def get_context_data(self):
        context = super(BeneficiaryOrgListView, self).get_context_data()
        context['title'] = 'Beneficiary List'
        return context

class BeneficiaryOrgDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'beneficiary/detail.html'
    
    def get_context_data(self):
        context = super(BeneficiaryOrgDetailView, self).get_context_data()
        context['title'] = 'Beneficiary List'
        return context
