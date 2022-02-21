from django import forms

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .validators import validate_url

# validate the input with any amount of validators you want

# the commented functions are a different way to do validation. 
# The current way allows the validation method (in validators.py) to be used in models.py and views.py
class sumbit_url_form(forms.Form):
    url = forms.CharField(
        label="", 
        validators=[validate_url],
        widget=forms.TextInput(
            attrs= {
                "placeholder": "Long URL",
                "class": "form-control"
            }
        )
    )

    # clean is called when form.cleaned_data is called in views
    # validates on the entire form
    """ def clean(self):
        cleaned_data = super(sumbit_url_form, self).clean()
        url = cleaned_data.get('url')
        print(url)

    # validates directly on the individual input field
    # if its not a proper url, will raise error
    def clean_url(self):
        url = self.cleaned_data.get("url")
        print(url)
        url_validator = URLValidator()
        try:
            url_validator(url)
        except: 
            raise forms.ValidationError("Invalid URL entered")
        return url """

""" def clean_url(self):
        url = self.cleaned_data['url']
        if "http" in url:
            return url
        return "http://" + url """