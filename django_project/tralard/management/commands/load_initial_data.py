import json
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    args = "<filename>"
    help = "Loads the initial data in to database"

    def handle(self, *args, **options):
        call_command("loaddata", "tralard/fixtures/users.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/province.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/district.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/ward.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/program.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/project.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/representative.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/project_feedback.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/sub_project.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/indicator.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/beneficiary.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/training_type.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/training.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/fund.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/disbursement.json", verbosity=0)
        call_command("loaddata", "tralard/fixtures/expenditure.json", verbosity=0)
        
        print("--------- DATA WAS LOADED SUCCESSFULLY ---------")
