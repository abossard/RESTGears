from django.conf.urls.defaults import *
from django.views.generic import list_detail
from publisher.models import NewsEntry, NewsImage, Article
from publisher.views import News, download_handler, ArticleView
from base import views as baseviews

#djangorestframework begins here
from djangorestframework.resources import ModelResource
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ListModelView, InstanceModelView
from base.utils import reverse

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

class ArticleResource(ModelResource):
    model = Article
    fields = (
        'id',
        'name',
        'content',
        'publish_on',
        )
    def url(self, instance):
        return reverse('article-instance', kwargs={'pk':instance.pk,}) 

class ArticleInstanceResource(ModelResource):
    model = Article
    fields = (
        'slug',
        'id',
        'name',
        'publish_on',
        'content',
        )

urlpatterns = patterns ('',
                        url(r'^$', News.as_view(), name ='news-overview'),
                        url(r'^index$', ListModelView.as_view(resource=EntryResource, ), name='news-index'),
                        url(r'^articles$', ListModelView.as_view(resource=ArticleResource, ), name='article-index'),
                        url(r'^articles/(?P<pk>\w+)$', ArticleView.as_view(resource=ArticleInstanceResource), name='article-instance'),
                        #url(r'^(?P<pk>[0-9]+)/$', InstanceModelView.as_view(resource=EntryResource)),
                        #url(r'^image/(?P<pk>\w+)$', download_handler, name='news-image'),
                        url(r'^image/(?P<pk>\w+)$', baseviews.ImageServeView.as_view(container=NewsImage), name='news-image'),
)
