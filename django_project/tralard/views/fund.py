from re import template
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, FormView
from tralard.forms.fund import FundForm

from tralard.models.fund import Fund 
from tralard.models.project import Project


class FundListAndCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new MedicalRecord
    """
    model = Fund
    form_class = FundForm
    template_name = "fund/list.html"

    def get_context_data(self, **kwargs):
        context = super(FundListAndCreateView, self).get_context_data(**kwargs)
        self.program_slug = self.kwargs['program_slug']
        self.project_slug = self.kwargs['project_slug']

        self.project = Project.objects.get(slug=self.project_slug)
        self.project_funds_qs = Fund.objects.filter(
            project__slug=self.project_slug
        )
        context["project"] = self.project
        context["funds"] = self.project_funds_qs
        context["fund_title"] = "add project fund"
        context["form"] = self.form_class
        context["title"] = "funds"
        return context


    def form_valid(self, form):
        form.save()
        return super(FundListAndCreateView, self).form_valid(form)



class FundDetailView(LoginRequiredMixin, DetailView):
    model = Fund
    context_object_name = 'fund'
    template_name = 'fund/detail.html'
    
    def get_context_data(self):
        context = super(FundDetailView, self).get_context_data()
        context['title'] = 'Funds'
        return context
