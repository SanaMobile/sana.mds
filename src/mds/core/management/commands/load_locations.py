"""
"""
from django.core.management.base import BaseCommand
from mds.utils import csv_import

class Command(BaseCommand):
    args = '<fname>'
    help = 'Loads location list formatted as <code>,<name>. <code> values must be unique'
            
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
    
    def _load_locations(self, fname, test=False):
        csv_import.load_locations(fname, test=test)

    def handle(self, *args, **options):
        try:
            test = args[1]
        except:
            test=False
        self._load_locations(args[0],test=test)
