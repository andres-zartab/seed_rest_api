from django.conf import settings
from django.db import models
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse

User = settings.AUTH_USER_MODEL

class BlogPost(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=120, blank=True, null=True)
    content     = models.TextField(max_length=120, blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    @property#NOTE: I do this because permissions.py needs a owner attribute
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        #NOTE:Using non rf reverse gives me '/api/postings/pk' but if I want to full url i have to use the rf reverse
        return api_reverse('api-postings:post-rud', kwargs={'pk': self.pk}, request=request)