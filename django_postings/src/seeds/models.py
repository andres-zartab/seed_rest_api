from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse

from postings.models import BlogPost

from seeds.api.utils import unique_slug_generator

class Seed(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name        = models.CharField(max_length=120, blank=True, null=True)
    slug        = models.SlugField(null=True, blank=True)
    gps_lat     = models.DecimalField(max_digits=9, decimal_places=6)
    gps_lon     = models.DecimalField(max_digits=9, decimal_places=6)
    #picture     = models.ImageField()
    active      = models.BooleanField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now_add=True)
    post        = models.ManyToManyField(BlogPost, blank=True)

    def __str__(self):
        return str(self.name)

    @property#NOTE: I do this because permissions.py needs a owner attribute
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        #NOTE:Using non rf reverse gives me '/api/postings/pk' but if I want to full url i have to use the rf reverse
        return api_reverse('api-seeds:seed-rud', kwargs={'pk': self.pk}, request=request)

def seed_pre_save_receiver(sender, instance, *args, **kwargs):
    print(instance)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.name:
        instance.name = 'S' + str(instance.__class__.objects.filter(user=instance.user.pk).count() + 1) + '_' + str(instance.user.username) 

pre_save.connect(seed_pre_save_receiver, sender=Seed)