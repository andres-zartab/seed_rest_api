from django.db.models import Q
from rest_framework import generics, mixins

from seed_app.models import Seed
from .serializers import SeedSerializer
from .permissions import IsOwnerOrReadOnly

class SeedAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = SeedSerializer

    def get_queryset(self):
        qs = Seed.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(title__contains=query)|
                Q(content__contains=query)
                ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class SeedRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = SeedSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Seed.objects.all()
    
    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}