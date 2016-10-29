"""
"""

from django.core.management.base import BaseCommand
from mds.utils import csv_import

class Command(BaseCommand):
    args = '<full path to file>'
    help = 'user csv list formatted as <command>,<username>,<password,villages|villages>. Username values must be unique.'

    def _load_users(self, fname):
        csv_import.load_users(fname)

    def handle(self, *args, **options):
        self._load_locations(args[0])
