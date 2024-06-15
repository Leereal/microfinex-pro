from django.core.management.base import BaseCommand

from apps.loans.engine import short_term_calculation

class Command(BaseCommand):
    help = 'Runs the short term calculation script'

    def handle(self, *args, **kwargs):
        short_term_calculation()