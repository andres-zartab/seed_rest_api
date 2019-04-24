from django.contrib.auth.models import User

from rest_framework import generics

from .serializers import GrowerSerializer

class GrowerListView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = GrowerSerializer

    def get_queryset(self):
        return User.objects.all()


class GrowerRetrieveView(generics.RetrieveAPIView):
    lookup_field        = 'pk'#NOTE: this is the default forthe rest_framework. This is the pk in the urls.py regexp
    serializer_class    = GrowerSerializer
    #permission_classes  = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return User.objects.all()