''' csv import utilities.
'''
import unicodecsv as csv

from django.contrib.auth.models import User

from mds.core.models import ANM, Location

# Locations file
# format as
# name,code
DEFAULT_CODE = 1
def load_locations(fname):
    """ Loads a list of locations from a csv file fomatted as
            name
        Code value may be provided or loaded as the default.

        'name' values should be unique.
    """
    with open(fname) as f:
        reader = csv.reader(f, delimiter=',')  
        for row in reader:
            code = row[0]
            name = row[1]
            try:
                location = Location.objects.get(code=code)
                created = False
            except:
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
            command = int(row[0])
            username=row[1]
            # 1 = add users
            if command == 1:
                password=row[2]
                location_str = row[3]
                locations = ()
                for code in location_str.split(';'):
                    locations.append(Location.objects.get(code=code))
                # create User
                user = User.objects.create_user(username=username, password=row[1])
                user.save()
                # Create ANM
                anm = ANM(user=user)
                for location in locations:
                    anm.locations.add(location)
                anm.save()
            #2=Modify(add villages),
            elif command == 2:
                anm = ANM(user__username=username)
                location_str = row[2]
                for location in location_str.split(';'):
                    anm.locations.add(location)
                anm.save()
            # 3=Modify(Replace villages)
            elif command == 3:
                anm = ANM(user__username=username)
                # remove villages
                for location in anm.locations.all():
                    anm.locations.remove(location)
                anm.save()
                location_str = row[2]
                for code in location_str.split(';'):
                    anm.locations.add(Location.objects.get(code=code))
                anm.save()
            # 4=remove locations
            elif command == 4:
                anm = ANM(user__username=username)
                location_str = row[2]
                for code in location_str.split(';'):
                    anm.locations.remove(Location.objects.get(code=code))
                anm.save()
