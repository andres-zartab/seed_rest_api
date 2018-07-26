from django.conf.urls import url, include

from .views import PlantApiView, PlantRudView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', PlantRudView.as_view(), name='plant-rud'),
    url(r'^$', PlantApiView.as_view(), name='plant-listcreate'),
]
