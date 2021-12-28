from django.db import models

def get_adjusted_name(user):
    name = user.first_name
    if name == 'Brian':
        name += ' ' + user.last_name
    return name

