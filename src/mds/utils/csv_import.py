''' csv import utilities.
'''
import unicodecsv as csv

from django.contrib.auth.models import User

from mds.core.models import ANM, Location

# Locations file
# format as
# name,code
DEFAULT_CODE = 1

def parse_locations(location_str):
    locations = [Location.objects.get(code=x) for x in location_str.split(';')]
    return locations                

def load_locations(fname,test=False):
    """ Loads a list of locations from a csv file fomatted as
            name
        Code value may be provided or loaded as the default.

        'name' values should be unique.
    """
    with open(fname) as f:
        reader = csv.reader(f, delimiter=',')
        index = 1  
        for row in reader:
            created = False
            try:
                code = row[0]
                name = row[1]
                try:
                    location = Location.objects.get(code=code)
                except:
                    location = Location()
                    location.code = code
                    created = True
                location.name = name
                if test:
                    print(location)
                else:
                    location.save()
            except Exception, e:
                print("Line %d. FAIL. created=%s. %s" % (index,created, e))
            index = index + 1
              
# Format as
# username,password,location;location
def load_users(fname):
    """ Loads a list of users from a csv file formatted as:
            username,password,locations
        where 'locations' is a semi colon separated list of location names.
    """
    with open(fname) as f:
        reader = csv.reader(f, delimiter=',')
        index = 1
        for row in reader:
            command = int(row[0])
            username=row[1]
            # 1 = add users
            try:
                if command == 1:
                    message = "Adding user %s" % username
                    password=row[2]
            
                    # create User
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    # Create ANM
                    anm = ANM(user=user)
                    anm.save()
                    # parse and add locations
                    location_str = row[3]
                    locations = parse_locations(location_str)
                    for location in locations:
                        anm.locations.add(location)
                    anm.save()
                #2=Modify(add villages),
                elif command == 2:
                    message = "Modifying user %s. Adding villages." % username
                    anm = ANM.objects.get(user__username=username)
                    location_str = row[2]
                    locations = parse_locations(location_str)
                    for location in locations:
                        anm.locations.add(location)
                    anm.save()
                # 3=Modify(Replace villages)
                elif command == 3:
                    message = "Modifying user %s. Replacing villages." % username
                    anm = ANM.objects.get(user__username=username)
                    # remove old locations
                    locations = anm.locations.all()
                    for location in locations:
                        anm.locations.remove(location)
                    anm.save()
                    # parse and add new locations
                    location_str = row[2]
                    locations = parse_locations(location_str)
                    for location in locations:
                        anm.locations.add(location)
                    anm.save()
                # 4=remove locations
                elif command == 4:
                    message = "Modifying user %s. Removing villages." % username
                    # Get ANM
                    anm = ANM.objects.get(user__username=username)
                    # parse and remove locations
                    location_str = row[2]
                    locations = parse_locations(location_str)
                    for location in locations:
                        anm.locations.remove(location)
                    anm.save()
            except Exception, e:
                    print("Line %d. FAIL. %s %s" % (index, message, e))
            index = index + 1
