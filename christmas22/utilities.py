from gift.models import Gift
from memory.models import Memory

import random

def user_has_gift(user):            # to be used in views to create a context variable for templates to use
    return len(Gift.objects.filter(receiver=user)) != 0

def get_random_memory():
    memories = Memory.objects.all()
    if len(memories) != 0:
        return random.choice(memories)
    else:
        return None
