from django.db import models

from shorten.models import Url

class analyticsManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, Url):
            obj, created = self.get_or_create(url=instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class analytics(models.Model):
    url = models.OneToOneField(Url, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True) # the last time the model was updated
    timestamp_created = models.DateTimeField(auto_now_add=True) # when model created

    objects = analyticsManager()

    def __str__(self):
        return f"{self.count}"