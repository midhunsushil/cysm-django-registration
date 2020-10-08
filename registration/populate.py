import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CySm.settings')

import django
django.setup()

from models import School_Info
from faker import Faker

fakegen = Faker()

def populate_School_Info(N=5):

    for _ in range(N):

        firstName = fakegen.first_name()
        lastName = fakegen.last_name()
        email = fakegen.free_email()

        name = models.CharField(max_length = 100)
        city = models.CharField(max_length = 20)
        state = models.CharField(max_length = 20)
        principal_name = models.CharField(max_length = 100)

        obj = Users(first_name = firstName, last_name = lastName, email = email)
        print("Saving Data Object =",obj)
        obj.save()

if __name__ == "__main__" :
    print("Starting to Populate Users Model...")
    populate(int(sys.argv[1]))
    print("Population Completed !!!")
