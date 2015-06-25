from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getLinks/(?P<city>.*)/(?P<category>.*)$', views.getLinks, name='getLinks'),
    url(r'^processFile/(?P<city>.*)/(?P<category>.*)$', views.processFile, name='processFile'),
    url(r'^genExcel/(?P<city>.*)/(?P<category>.*)$', views.genExcel, name='genExcel'),
    url(r'^getPos/(?P<city>.*)/(?P<category>.*)$', views.getPos, name='getPos'),
    url(r'^delAll/', views.delAll, name='delAll'),
    url(r'^check/', views.check, name='check'),
    url(r'^reco/', views.reco, name='reco'),
    url(r'^testSend/(?P<A>.*)/(?P<B>.*)$', views.testSend, name='testSend'),
    url(r'^getItems/', views.getItems, name='getItems'),
]
