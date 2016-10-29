"""
"""

from django.core.management.base import BaseCommand
from mds.utils import csv_import

class Command(BaseCommand):
    args = '<fname>'
    help = 'user csv list formatted as <command>,<username>,<password,villages|villages>. Username values must be unique.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
    
    def _load_users(self, fname):
        csv_import.load_users(fname)

    def handle(self, *args, **options):
        self._load_users(args[0])
