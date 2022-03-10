import os
from datetime import datetime

from django.conf import settings

from core.celery import app as celery_app

from tralard.utils import IndicatorReportBuild


@celery_app.task()
def build_indicator_report(project_slug):
    from tralard.models import Indicator

    indicators = Indicator.objects.filter(indicator_related_subcomponents__project__slug=project_slug)

    temporary_dir = f"{settings.MEDIA_ROOT}/temp/reports"

    if not os.path.exists(temporary_dir):
        os.makedirs(temporary_dir)

    timestamp = datetime.now().strftime("%H_%M_%S_%f")

    # Create a unique filename for the pdf to be created
    filename = f"indicator_report_{timestamp}.pdf"

    # Create a full path to the directory containing to save the file
    save_to_dir = f"{temporary_dir}/{filename}"

    builder = IndicatorReportBuild(save_to_dir, indicators)
    builder.build_doc()

    return {"task_type": "indicator_report", "result": {"dir": temporary_dir, "filename": filename}}
