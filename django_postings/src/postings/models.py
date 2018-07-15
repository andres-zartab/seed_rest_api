from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class BlogPost(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=120, blank=True, null=True)
    content     = models.TextField(max_length=120, blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
