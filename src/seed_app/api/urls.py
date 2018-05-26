from django.conf.urls import url

from .views import SeedRudView, SeedAPIView

urlpatterns = [
    url(r'^$', SeedAPIView.as_view(), name='seed-listcreate'),
    url(r'^(?P<pk>\d+)/$', SeedRudView.as_view(), name='seed-rud'),
]