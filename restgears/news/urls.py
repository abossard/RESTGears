from django.conf.urls.defaults import *
from django.views.generic import list_detail
from news.models import Entry
from news import views
from base import views as baseviews

#djangorestframework begins here
from djangorestframework.resources import ModelResource
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ListModelView, InstanceModelView

class EntryResource(ModelResource):
    model = Entry
    fields = (
        'name',
        'teaser',
        'content',
        ('category',
         ('name',),),
        ('images',
         ('description', 'url',),),
        'publish_on',
        #'url',
        )

urlpatterns = patterns ('',
                        url(r'^$', ListModelView.as_view(resource=EntryResource, ), name='news-index'),
                        #url(r'^(?P<pk>[0-9]+)/$', InstanceModelView.as_view(resource=EntryResource)),
                        (r'^image/(?P<pk>\w+)$', views.download_handler),
)
