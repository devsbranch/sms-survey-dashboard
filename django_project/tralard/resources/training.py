# coding=utf-8
"""
Training model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.training import Training, Attendance, TrainingType


class TrainingResource(resources.ModelResource):
    class Meta:
        model = Training
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "sub_project",
            "title",
            "training_type",
            "start_date",
            "end_date",
            "notes",
            "moderator",
            "completed",
        )


class AttendanceResource(resources.ModelResource):
    class Meta:
        model = Attendance
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "sub_project",
            "title",
            "training_type",
            "start_date",
            "end_date",
            "notes",
            "moderator",
            "completed",
        )


class TrainingTypeResource(resources.ModelResource):
    class Meta:
        model = TrainingType
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = ("id", "name")
