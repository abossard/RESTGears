from django.conf.urls.defaults import *
from django.views.generic import list_detail
from gallery.models import Photo
from gallery.handlers import PhotoHandler
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from piston.doc import documentation_view


photo_info = {
        "queryset" : Photo.objects.all(),
}

auth = HttpBasicAuthentication(realm='Gallery Realms')
photo_handler = Resource(handler=PhotoHandler, authentication=auth)

urlpatterns = patterns ('',
    (r'^$', list_detail.object_list, photo_info, 'photo-index'),
    url(r'^api$', photo_handler, { 'emitter_format': 'json' }),
)
