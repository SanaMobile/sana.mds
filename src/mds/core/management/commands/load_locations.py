"""
"""
from django.core.management.base import BaseCommand
from mds.utils import csv_import

class Command(BaseCommand):
    args = '<full path to file>'
    help = 'Loads location list formatted as code, name. Code values must be unique'

    def _load_locations(self, fname):
        csv_import.load_locations(fname)

    def handle(self, *args, **options):
        self._load_locations(args[0])
