from django.db.models import Q
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from seeds.models import Seed
from .permissions import IsOwnerOrReadOnly
from .serializers import SeedSerializer


class SeedApiView(generics.ListAPIView, mixins.CreateModelMixin):
    lookup_field = 'pk'#NOTE: this is the default forthe rest_framework. This is the pk in the urls.py regexp
    serializer_class = SeedSerializer
    #permission_classes = [IsAuthenticated] #NOTE:Here I can customize permissions as desired
    
    def get_queryset(self):
        print(self.request.auth)
        print(self.request.user)
        qs = Seed.objects.all()
        #qs = Seed.objects.filter(user=self.request.user) #NOTE:IF I WANT TO FILTER IT
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query)|
                Q(active__icontains=query)
                ).distinct()
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)#NOTE:This handles the mixin

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class SeedRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field        = 'pk'#NOTE: this is the default forthe rest_framework. This is the pk in the urls.py regexp
    serializer_class    = SeedSerializer
    permission_classes  = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Seed.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}
    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return BlogPost.objects.get(pk=pk) NOTE: this overrides lookup_field

    
