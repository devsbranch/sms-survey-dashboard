import json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

from tralard.models.fund import (
    Fund, 
    Expenditure,
    Disbursement 
)


class Command(BaseCommand):
    args = "<filename>"
    help = "Loads the initial data in to database"

    def handle(self, *args, **options):
        if settings.DEBUG:
            call_command("loaddata", "tralard/fixtures/dev/users.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/province.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/district.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/ward.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/indicator.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/indicator_unit_of_measure.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/indicator_target.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/indicator_target_value.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/project.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/subcomponent.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/project_feedback.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/sub_project.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/beneficiary.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/training_type.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/training.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/fund.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/disbursement.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/dev/expenditure.json", verbosity=0)

            for fund in Fund.objects.all():
                fund.save()

            for disbursement in Disbursement.objects.all():
                disbursement.save()

            for expenditure in Expenditure.objects.all():
                expenditure.save()

            print("---------FUND DISBURSEMENT AND EXPENSE BALANCE SIGNALS UPDATED ---------")
        else:
            call_command("loaddata", "tralard/fixtures/prod/users.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/prod/province.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/prod/district.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/prod/ward.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/prod/indicator.json", verbosity=0)
            call_command("loaddata", "tralard/fixtures/prod/project.json", verbosity=0)

        print("--------- DATA WAS LOADED SUCCESSFULLY ---------")
