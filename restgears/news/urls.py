from django.conf.urls.defaults import *
from django.views.generic import list_detail
from news.models import Entry

news_info = {
        "queryset" : Entry.objects.all(),
}

urlpatterns = patterns ('',
    (r'^$', list_detail.object_list, news_info, 'news-index'),
)
