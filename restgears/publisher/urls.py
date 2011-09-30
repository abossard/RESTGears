from django.conf.urls.defaults import *
from django.views.generic import list_detail
from publisher.models import NewsEntry, NewsImage
from publisher.views import News, download_handler
from base import views as baseviews

#djangorestframework begins here
from djangorestframework.resources import ModelResource
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ListModelView, InstanceModelView

class EntryResource(ModelResource):
    model = NewsEntry
    fields = (
        'id',
        'name',
        'teaser',
        'content',
        'image_url',
        'thumb_image_url',
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
                        url(r'^image/(?P<pk>\w+)$', baseviews.ImageServeView.as_view(container=NewsImage), name='news-image'),
)
