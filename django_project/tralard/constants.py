from django.utils.translation import gettext_lazy as _

ZMK = 'ZMK'
USD = 'USD'
GBP = 'GBP'
EU = 'EU'

CURRENCY_CHOICES = [
    (ZMK, 'ZMK'), 
    (USD, 'USD'),
    (GBP, 'GBP'),
    (EU, 'EU')
    ]

MAP_LAYER_CHOICES = [
    "CartoDB Positron",
    "Open Street Map",
    "Stamen Terrain",
    "Stamen Toner",
    "Stamen Watercolor",
    "CartoDB Dark_Matter",
    ]

GENDER_CHOICES = (
    ("Male", _("Male")),
    ("Female", _("Female")),
    ("Transgender", _("Transgender")),
    ("Other", _("Other"))
    )

PROJECT_STATUS_CHOICES = (
    ("Identified", _("Identified")),
    ("In Progress", _("In Progress")),
    ("Completed", _("Completed"))
    )

CUSTOM_MAP_SETTINGS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocation", [-15.7177013, 28.6300491]),
    ),
}