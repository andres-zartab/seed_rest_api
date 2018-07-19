from django.db.models import Q
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from postings.models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer

class BlogPostApiView(generics.ListAPIView, mixins.CreateModelMixin):
    lookup_field = 'pk'#NOTE: this is the default forthe rest_framework. This is the pk in the urls.py regexp
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated] #NOTE:Here I can customize permissions as desired
    
    def get_queryset(self):
        print(self.request.auth)
        print(self.request.user)
        qs = BlogPost.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)
                ).distinct()
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def post(self, request, *args, **kwargs):
    #     return NOTE:THis allows POST but it is the hard way

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)#NOTE:This handles the mixin
    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field        = 'pk'#NOTE: this is the default forthe rest_framework. This is the pk in the urls.py regexp
    serializer_class    = BlogPostSerializer
    permission_classes  = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return BlogPost.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}
    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return BlogPost.objects.get(pk=pk) NOTE: this overrides lookup_field

    
