from rest_framework import generics, mixins

from postings.models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostApiView(generics.ListAPIView, mixins.CreateModelMixin):
    lookup_field = 'pk'#NOTE: this is the default forthe rest_framework. This is the pk in the urls.py regexp
    serializer_class = BlogPostSerializer
    
    def get_queryset(self):
        return BlogPost.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def post(self, request, *args, **kwargs):
    #     return NOTE:THis allows POST but it is the hard way

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)#NOTE:This handles the mixin

class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'#NOTE: this is the default forthe rest_framework. This is the pk in the urls.py regexp
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return BlogPost.objects.get(pk=pk) NOTE: this overrides lookup_field

    
