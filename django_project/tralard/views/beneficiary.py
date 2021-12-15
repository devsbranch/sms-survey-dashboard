"""
Please note that this logic will be housed at dj_beneficiary installable app.
hence all logic partaining to beneficiary will live in that external application.
"""

# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from dj_beneficiary import Beneficiary, Ward

