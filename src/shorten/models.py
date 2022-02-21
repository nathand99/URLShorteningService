from django.db import models

from .utils import create_code
from django.conf import settings

from .validators import validate_url

#from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse # we are using django_hosts version of reverse instead

MAX_SHORTENED = getattr(settings, "MAX_SHORTENED", 15) # gets MAX_SHORTENED var from settings.py. 
            # = settings.MAX_SHORTENED - not portable version. ok if not going to reuse this code
# If that var doesnt exist, the default is 15


# model makes a place to add data
# Create your models here.
# shorten is an app
#Url also has pk (primary key) and id variables by default (eg self.id)

# examples of using model managers - not that practical - but good to know
class UrlManager(models.Manager):
    # print(Url.objects.all()) - would print out all objects created
    # we can modify what "all" means here in the function below
    def all(self, *args, **kwargs):
        query_set = super(UrlManager, self).all(*args, **kwargs)
        query_set = query_set.filter(active=True) # take out all inactive objects
        return query_set

    # refresh all shortened codes to new codes
    def refresh_shortened(self, num=None):
        # get all objects - remember we changed all above - so we need to use another way to
        # truely get all objects. This gets all objects with id >= 1
        count = 0
        query_set = Url.objects.filter(id__gte=1)
        # number of ids to refresh. Will only refresh the first "num" ids (sorted in reverse id order (-id) if num is not None)
        if num is not None and isinstance(num, int):
            qs = qs.order_by("-id")[:num]
        for q in query_set:
            q.shortened = create_code(q)
            q.save()
            count += 1
        return f"new codes made: {count}"

class Url(models.Model):
    url = models.CharField(max_length=220, validators=[validate_url])
    shortened = models.CharField(max_length=MAX_SHORTENED, unique=True, blank=True) # blank = true - not required to input but its required in the database
    last_updated = models.DateTimeField(auto_now=True) # the last time the model was updated
    timestamp_created = models.DateTimeField(auto_now_add=True) # when model created
    active = models.BooleanField(default=True)

    objects = UrlManager() # use the UrlManager() definition of all for objects

    # built into the model class - this saves a new object. We override
    def save(self, *args, **kwargs):
        if self.shortened == None or self.shortened == "":
            self.shortened = create_code(self) # now when save we will generate a new random shortened
        if not "http" in self.url:
            self.url = "http://" + self.url
        return super(Url, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)

    def get_shortened_url(self):
        url_path = reverse("shortened", kwargs={'shortened': self.shortened}, host="www", scheme="http", port="8000")
        return url_path

