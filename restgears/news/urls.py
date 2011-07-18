from django.conf.urls.defaults import *
from django.views.generic import list_detail
from news.models import Entry, Image
from news.views import News, download_handler
from base import views as baseviews

#djangorestframework begins here
from djangorestframework.resources import ModelResource
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ListModelView, InstanceModelView

class EntryResource(ModelResource):
    model = Entry
    fields = (
        'id',
        'name',
        'teaser',
        'content',
        ('images',
         ('description', 'url','id','orderindex'),),
        'publish_on',
        #'url',
        )

urlpatterns = patterns ('',
                        url(r'^$', News.as_view(), name ='news-overview'),
                        url(r'^index$', ListModelView.as_view(resource=EntryResource, ), name='news-index'),
                        #url(r'^(?P<pk>[0-9]+)/$', InstanceModelView.as_view(resource=EntryResource)),
                        #url(r'^image/(?P<pk>\w+)$', download_handler, name='news-image'),
                        url(r'^image/(?P<pk>\w+)$', baseviews.ImageServeView.as_view(container=Image), name='news-image'),
)
