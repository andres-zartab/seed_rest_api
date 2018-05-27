from django.conf import settings
from django.db import models
from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse

# Create your models here.
class Seed(models.Model):
    # pk aka id --> numbers
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seeds') 
    title       = models.CharField(max_length=120, null=True, blank=True)
    content     = models.TextField(max_length=120, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
        
    @property
    def owner(self):
        return self.user
    
    def get_absolute_url(self, request=None):
        return reverse('api-seed_app:seed-rud', kwargs={'pk': self.pk}, request=request)
    
    def get_api_uri(self, request=None):
        return api_reverse('api-seed_app:seed-rud', kwargs={'pk': self.pk}, request=request)
