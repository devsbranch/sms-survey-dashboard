from django.urls import reverse_lazy
from django.shortcuts import (
    redirect,
    get_object_or_404,
)
from django.views.generic import (
    UpdateView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tralard.models.profile import Profile
from tralard.forms.profile import ProfileForm
from tralard.utils import user_profile_update_form_validator


# @login_required(login_url="/login/")
# def user_profile_update(request):
#     from django.http import JsonResponse
#     if request.method == 'POST':
#         obj=MyObj.objects.get(pk=furtherData_id)
#         obj.data=request.POST['furtherData']
#         obj.save()
#         return JsonResponse({'result':'ok'})
#     else:
#         return JsonResponse({'result':'nok'}


@login_required(login_url="/login/")
def user_profile_update(request, project_slug, program_slug):
    form = ProfileForm()
    training = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("tralard:home"))
