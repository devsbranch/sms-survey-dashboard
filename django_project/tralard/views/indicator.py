# -*- coding: utf-8 -*-
__author__ = "Alison Mukoma <mukomalison@gmail.com>"
__date__ = "31/12/2021"
__revision__ = "$Format:%H$"
__copyright__ = "sonlinux bei DigiProphets 2021"
__annotations__ = "Written from 31/12/2021 23:34 AM CET -> 01/01/2022, 00:015 AM CET"

"""
View classes for a SubProject
"""

from django.conf import settings
from django.contrib import messages

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

from celery.result import AsyncResult

from tralard.models import Indicator, IndicatorTarget, IndicatorTargetValue, IndicatorUnitOfMeasure
from tralard.forms import (
    IndicatorForm,
    IndicatorTargetForm,
    IndicatorTargetValueForm,
    IndicatorUnitOfMeasureForm,
)
from tralard.tasks import build_indicator_report


@login_required(login_url="/login/")
def indicator_report(request, program_slug):
    if request.is_ajax():
        try:
            task = build_indicator_report.delay(program_slug)

            if isinstance(task, AsyncResult):
                return JsonResponse({"task_id": task.task_id})
            else:
                return JsonResponse({"message": "An error occured"}, status=500)

        except:
            return JsonResponse({"task_id": task.task_id})
    else:
        JsonResponse({"message": "unknown request"})


@login_required(login_url="/login/")
def poll_state(request, task_id):
    if request.is_ajax():
        task = AsyncResult(task_id)

        if task.state == "SUCCESS":
            filename = task.result["result"]["filename"]

            download_url = f"{settings.MEDIA_URL}temp/reports/{filename}"
            body = {
                "state": task.state,
                "download_url": download_url,
                "filename": filename,
            }
            return JsonResponse(body, status=200)

        elif task.state == "PENDING":
            body = {"state": task.state}
            return JsonResponse(body, status=200)

        else:
            return JsonResponse({"error": "Bad request"}, status=400)
    else:
        return JsonResponse({"error": "Bad request"}, status=400)


@login_required(login_url="/login/")
def create_indicator(request, program_slug):
    if request.method == "POST":
        form = IndicatorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The Indicator was created successfully.")
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )
        else:
            messages.error(
                request,
                "The Indicator could not be created. Ensure the form data is valid",
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )


@login_required(login_url="/login/")
def create_indicator_target(request, program_slug):
    if request.method == "POST":
        form = IndicatorTargetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The Indicator Target was created successfully.")
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )
        else:
            messages.error(
                request,
                "The Indicator Target could not be created. Ensure the form data is valid",
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )


@login_required(login_url="/login/")
def update_indicator_target(request, program_slug, target_id):
    indicator_target_obj = get_object_or_404(IndicatorTarget, pk=target_id)
    if request.is_ajax():
        obj_to_dict = model_to_dict(indicator_target_obj)

        return JsonResponse(obj_to_dict, status=200)

    if request.method == "POST":
        form = IndicatorTargetForm(request.POST, instance=indicator_target_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "The Indicator Target was updated successfully.")
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )
        else:
            messages.error(
                request,
                "The Indicator Target could not be created. Ensure the form data is valid",
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )


@login_required(login_url="/login/")
def create_indicator_target_value(request, program_slug):

    if request.method == "POST":
        form = IndicatorTargetValueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "The Indicator Target Values where created successfully."
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )
        else:
            messages.error(
                request,
                "The Indicator Target value could not be created. Ensure the form data is valid",
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )


@login_required(login_url="/login/")
def update_indicator_target_value(request, program_slug, indicator_target_value_id):
    indicator_target_value_obj = get_object_or_404(
        IndicatorTargetValue, pk=indicator_target_value_id
    )
    if request.is_ajax():
        obj_to_dict = model_to_dict(indicator_target_value_obj)

        return JsonResponse(obj_to_dict, status=200)

    if request.method == "POST":
        form = IndicatorTargetValueForm(request.POST, instance=indicator_target_value_obj)
        if form.is_valid():
            form.save()
            messages.success(
                request, "The Indicator Target Values where created successfully."
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )
        else:
            messages.error(
                request,
                "The Indicator Target value could not be created. Ensure the form data is valid",
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )


@login_required(login_url="/login/")
def create_indicator_unit_of_measure(request, program_slug):
    if request.method == "POST":
        form = IndicatorUnitOfMeasureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The Unit of measure was created successfully.")
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )
        else:
            messages.error(
                request,
                "The Indicator Unit of Measure could not be created. Ensure the form data is valid",
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )


@login_required(login_url="/login/")
def update_indicator_unit_of_measure(request, program_slug, indicator_target_unit_id):
    indicator_unit_of_measure_obj = IndicatorUnitOfMeasure.objects.get(pk=indicator_target_unit_id)
    if request.is_ajax():
        obj_to_dict = model_to_dict(indicator_unit_of_measure_obj)

        return JsonResponse(obj_to_dict, status=200)

    if request.method == "POST":
        form = IndicatorUnitOfMeasureForm(request.POST, instance=indicator_unit_of_measure_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "The Unit of measure was updated successfully.")
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )
        else:
            messages.error(
                request,
                "The Indicator Unit of Measure could not be updated. Ensure the form data is valid",
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )


@login_required(login_url="/login/")
def update_indicator(request, program_slug, indicator_slug=None):
    if request.method == "POST":
        indicator_obj = Indicator.objects.get(slug=indicator_slug)
        form = IndicatorForm(request.POST, instance=indicator_obj)

        if form.is_valid():
            form.save()
            messages.success(request, "The Indicator was updated successfully.")
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )
        else:
            messages.error(
                request,
                "The Indicator could not be updated. Ensure the form data is valid",
            )
            return redirect(
                reverse_lazy(
                    "tralard:program-detail",
                    kwargs={
                        "program_slug": program_slug,
                    },
                )
            )

@login_required(login_url="/login/")
def delete_indicator(request, program_slug, indicator_slug=None):
    if request.method == "POST":
        indicator_obj = get_object_or_404(Indicator, slug=indicator_slug)
        indicator_obj.delete()

        messages.success(request, "The Indicator was deleted successfully.")
        return redirect(
            reverse_lazy(
                "tralard:program-detail",
                kwargs={
                    "program_slug": program_slug,
                },
            )
        )
