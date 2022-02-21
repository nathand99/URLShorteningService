from django.core.management.base import BaseCommand, CommandError
from shorten.models import Url

class Command(BaseCommand):
    help = 'refreshes all shortened codes'


    # add a (optional) num argument 
    def add_arguments(self, parser):
        parser.add_argument('--num', type=int)

    # --num means that the num argument is not required.
    # to use python3 manage.py refreshcodes --num 10
    # if it was just num, then its required and you dont need to write num 
    # eg python3 manage.py refreshcodes 10
    # we can put more arguments in if we want

    def handle(self, *args, **options):
        return Url.objects.refresh_shortened(num=options['num'])