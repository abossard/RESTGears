from django.conf.urls.defaults import *
from django.views.generic import list_detail
from documents.models import Document

document_info = {
        "queryset" : Document.objects.all(),
}

urlpatterns = patterns ('',
    (r'^$', list_detail.object_list, document_info),
)
