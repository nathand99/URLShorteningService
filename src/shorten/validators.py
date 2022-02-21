from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# these functions validate the url in form forms.py and models.py
# a url without http:// at the front is considered to be invalid even though it is valid
# this function adds http:// on the front to make sure that its valid
# both flags must be False to raise error. 
# if good the first time, it will fail the second time (http://http://google.com)
# if bad the first time it will be good the second time
# in both these instaces, both flags will NOT be both False

def validate_url(value):
    url_validator = URLValidator()
    reg_val = value
    if "http" in reg_val:
        new_value = reg_val
    else:
        new_value = 'http://' + value
    try:
        url_validator(new_value)
    except:
        raise ValidationError("Invalid URL for this field")
    return new_value

""" def validate_url(value):
    url_validator = URLValidator()
    flag1 = False
    flag2 = False
    # try url - if not valid then add http:// onto the front. If valid then the next try will fail
    try:
        url_validator(value)
    except:
        flag1 = True
    new_url = "http://" + value
    # try new url - if good then
    try:
        url_validator(new_url)
    except: 
        flag2 = True
    
    if flag1 == False and flag2 == False or flag1 == True and flag2 == True:
        raise ValidationError("Invalid URL entered")
    return value """

# more validators if you want