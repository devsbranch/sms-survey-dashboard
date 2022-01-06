from re import template
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from tralard.models.training import Training
from tralard.models.beneficiary import Beneficiary
from django.contrib.auth.decorators import login_required
from django.core import serializers
from tralard.training.forms import TrainingForm

import json

class TrainingListView(LoginRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    template_name = 'training/list.html'

    def get_success_url(self):
        return reverse_lazy("tralard:training-list", kwargs={
            "program_slug": self.kwargs.get("program_slug", None),
            "project_slug": self.kwargs.get("project_slug", None),
        })

    def get_context_data(self):
        context = super(TrainingListView, self).get_context_data()
        context['title'] = 'Training'
        context['total_beneficiaries'] = Beneficiary.objects.all().count()
        context['program_slug'] = self.kwargs.get("program_slug", None)
        context['project_slug'] = self.kwargs.get("project_slug", None)
        context['trainings'] = Training.objects.all()
        return context


@login_required(login_url="/login/")
def training_delete(request, program_slug, project_slug, training_entry_slug):
    training = Training.objects.get(slug=training_entry_slug)
    training.delete()
    return redirect(reverse_lazy("tralard:training-list", kwargs={
        "program_slug": program_slug,
        "project_slug": project_slug,
    }))


# Work in Progress
@login_required(login_url="/login/")
def training_fetch(request, program_slug, project_slug, training_entry_slug):
    training = get_object_or_404(Training, slug=training_entry_slug)
    jsonified_training_detail = serializers.serialize('json', [training])
    struct = json.loads(jsonified_training_detail)
    training = json.dumps(struct[0])
    response = {
        'response': training,
    }
    return HttpResponse(response['response'])

 # temporal view for previewing templates
@login_required(login_url="/login/")
def template_testing(request):
    return render(request, "tralard/dashboard-datatable-variationss.html")
