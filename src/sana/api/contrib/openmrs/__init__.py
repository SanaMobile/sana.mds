''' The OpenMRS request handlers and utilities'''

from openmrs16 import OpenMRS as OpenMRS16
from openmrs19 import OpenMRS as OpenMRS19

CURRENT_VERSION=1.9
""" Default current version for the API. Can be overridden. """



def get_opener(version=CURRENT_VERSION):
    pass

