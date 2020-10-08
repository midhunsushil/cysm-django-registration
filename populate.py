import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CySm.settings')

import django
django.setup()

# Fake Population Script
import random
from my_first_app.models import *
from faker import Faker

def random_with_N_digits(min_digits ,max_digits):
    range_start = 10**(min_digits-1)
    range_end = (10**max_digits)-1
    return random.randint(range_start, range_end)

fakegen = Faker()

def populate(N=5):

    for _ in range(N):

        # Populate Login Model
        fake_username = fakegen.profile(fields= ['username'], sex=None).get('username')
        fake_password = fakegen.password(int(random.random()*20)+8)
        login = Login.objects.get_or_create(username=fake_username, password=fake_password)[0]
        login.save()
        # Populate User_Detail Model
        fake_email = fakegen.profile(fields= ['mail'], sex=None).get('mail')
        fake_dob = fakegen.profile(fields= ['birthdate'], sex=None).get('birthdate')
        fake_phone = random_with_N_digits(8,10)
        user_info = User_Detail.objects.get_or_create(username=login, email=fake_email, dob = fake_dob, phone_no= fake_phone)[0]

if __name__ == '__main__':
    print("Populating my_first_app.models started...")
    populate(20)
    print("Population Completed !")
