from tralard.models.profile import Profile
from tralard.forms.profile import ProfileForm
from tralard.utils import user_profile_update_form_validator
from django.db.models import Sum
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
from tralard.models.program import Program
from tralard.models.project import Project
from tralard.models.fund import Fund
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    model = Profile
    template_name = 'index.html'
    
    def get_context_data(self):
        context = super(HomeTemplateView, self).get_context_data()
        try:
            self.current_user_profile = Profile.objects.get(user=self.request.user)
        except:
            self.current_user_profile = None
        self.total_project_funds = Fund.objects.all().aggregate(Sum('amount'))
        self.cleaned_total_project_funds = self.total_project_funds['amount__sum']
        self.user_profile_utils = user_profile_update_form_validator(self.request.POST, self.request.user)
        context['title'] = 'Program: Tralard'
        context['program_list'] = Program.objects.all().order_by('-started')[:5]
        context['project_count'] = Project.objects.all().count()
        context['user_roles'] = self.user_profile_utils[0]
        context['profile'] = self.user_profile_utils[1]
        context['profile_form'] = self.user_profile_utils[2]
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


