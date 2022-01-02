from re import template
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from tralard.models.training import Training
from django.contrib.auth.decorators import login_required

from tralard.forms.training_forms import TrainingForm

class TrainingListView(LoginRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    template_name = 'tralard/training_list.html'

    def get_success_url(self):
        return reverse_lazy("tralard:training-list")

    def get_context_data(self):
        context = super(TrainingListView, self).get_context_data()
        context['title'] = 'Training'
        context['training_array_length'] = len([training.id for training in Training.objects.all()])
        context['trainings'] = Training.objects.all()
        return context


@login_required(login_url="/login/")
def training_delete(request, training_slug):
    training = Training.objects.get(slug=training_slug)
    training.delete()
    return redirect(reverse_lazy("tralard:training-list"))

@login_required(login_url="/login/")
def template_testing(request):
    return render(request, "tralard/dashboard-datatable-variationss.html")

class TrainingCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Training object.
    """
    model = Training
    form_class = TrainingForm
    template_name = "tralard/training-create.html"
    
    def get_success_url(self):
        return reverse_lazy("tralard:training-list")

    def get_context_data(self, **kwargs):
        context = super(TrainingCreateView, self).get_context_data(**kwargs)
        context["title"] = "create new Training"
        return context
