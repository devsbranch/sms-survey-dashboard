from django.db.models import Sum
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.models.program import Program
from tralard.models.fund import Fund
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(HomeTemplateView, self).get_context_data()
        self.total_project_funds = Fund.objects.all().aggregate(Sum('amount'))
        self.cleaned_total_project_funds = self.total_project_funds['amount__sum']

        context['title'] = 'Program: Tralard'
        context['program_list'] = Program.objects.all().order_by('-started')[:5]
        context['program_count'] = Program.objects.all().count()
        context['total_project_funds'] = self.cleaned_total_project_funds
        context['subproject_count'] = SubProject.objects.all().count()
        context['beneficiary_count'] = Beneficiary.objects.all().count()
        return context

class ProjectListView(LoginRequiredMixin, TemplateView):
    template_name = 'tralard/dashboard-crm-deal.html'

    def get_context_data(self):
        context = super(ProjectListView, self).get_context_data()
        context['title'] = 'Projects'
        return context


