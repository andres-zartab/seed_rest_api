from django.conf.urls import url, include

from .views import GrowerListView, GrowerRetrieveView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', GrowerRetrieveView.as_view(), name='grower-get'),
    url(r'^$', GrowerListView.as_view(), name='grower-list'),
]
