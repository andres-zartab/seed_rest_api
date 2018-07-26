from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse

from seeds.models import Seed

#from seeds.api.utils import unique_slug_generator

class Plant(models.Model):
    """
    This class represents a Plant which is any item the users want to trade
    """
    seed        = models.ForeignKey(Seed, on_delete=models.CASCADE)
    name        = models.CharField(max_length=120, blank=True, null=True)
    about       = models.CharField(max_length=120, blank=True, null=True)
    category    = models.CharField(max_length=120, blank=True, null=True)
    slug        = models.SlugField(null=True, blank=True)
    #picture     = models.ImageField()
    active      = models.BooleanField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.category)

    @property#NOTE: I do this because permissions.py needs a owner attribute
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        #NOTE:Using non rf reverse gives me '/api/postings/pk' but if I want to full url i have to use the rf reverse
        return api_reverse('api-seeds:seed-rud', kwargs={'pk': self.pk}, request=request)

def plant_pre_save_receiver(sender, instance, *args, **kwargs):
    user_pk         = instance.user.pk
    user_username   = instance.user.username
    qs              = instance.__class__.objects.filter(user=user_pk)
    if not instance.name:
        instance.name = 'S' + str(qs.count() + 1) + '_' + str(user_username) 
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    

pre_save.connect(plant_pre_save_receiver, sender=Plant)