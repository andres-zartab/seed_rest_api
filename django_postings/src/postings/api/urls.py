from django.conf.urls import url, include

from .views import BlogPostRudView, BlogPostApiView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post-rud'),
    url(r'^$', BlogPostApiView.as_view(), name='post-create'),
]
