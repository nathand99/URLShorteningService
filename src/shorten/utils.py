# utility functions

import random 
import string

# from shorten.models import Url - not allowed becasue of circular dependancies
from django.conf import settings

MIN_SHORTENED = getattr(settings, "MIN_SHORTENED", 6)

# generates a random sequence of characters
def code_generator(size=MIN_SHORTENED, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_code(instance, size=6):
    # generate a code
    new_code = code_generator(size=size)
    # check that this code has not been used before
    url_class = instance.__class__ # get class - allows us to use methods from the class. will use objects.filter
    # go through all objects - look at all shortened codes - if a shortened already exists, 
    # then do the function again to generate a unique code, return when unique
    query_set = url_class.objects.filter(shortened=new_code).exists() # bool
    if query_set:
        return create_code(instance, size=6)
    return new_code