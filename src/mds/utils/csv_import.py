''' csv import utilities.
'''
import unicodecsv as csv

from django.contrib.auth.models import User

from mds.core.models import ANM, Location

# Locations file
# format as
# name,code
DEFAULT_CODE = 1
def load_locations(fname, code=DEFAULT_CODE):
    """ Loads a list of locations from a csv file fomatted as
            name
        Code value may be provided or loaded as the default.

        'name' values should be unique.
    """
    with open(fname) as f:
        reader = csv.reader(f, delimiter=',')  
        for row in reader:
            location, created = Location.objects.get_or_create(name=row[0], code=code)
                  
              
# Format as
# username,password,location;location
def load_users(fname):
    """ Loads a list of users from a csv file formatted as:
            username,password,locations
        where 'locations' is a semi colon separated list of location names.
    """
    with open(fname) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # create User
            user = User.objects.create_user(username=row[0], password=row[1])
            user.save()
            # Create ANM
            anm = ANM(user=User)
            location_str = row[2]
            for location_name in location_str.split(';'):
                location = Location.objects.get(name=location_name)
                anm.add(location)
            anm.save()
