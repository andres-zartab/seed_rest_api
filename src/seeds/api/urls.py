from django.conf.urls import url, include

from .views import SeedApiView, SeedRudView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', SeedRudView.as_view(), name='seed-rud'),
    url(r'^$', SeedApiView.as_view(), name='seed-listcreate'),
]
