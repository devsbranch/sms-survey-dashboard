import django_filters

from tralard.models import Training, TrainingType


class TrainingFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Training
        fields = ["title", "training_type", "completed"]
