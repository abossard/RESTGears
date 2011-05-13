from django.conf.urls.defaults import *
from django.views.generic import list_detail
from gallery.models import Photo
from gallery.handlers import PhotoHandler
from piston.resource import Resource

photo_info = {
        "queryset" : Photo.objects.all(),
}

photo_handler = Resource(PhotoHandler)


urlpatterns = patterns ('',
    (r'^$', list_detail.object_list, photo_info, 'photo-index'),
    url(r'^api$', photo_handler, { 'emitter_format': 'json' }),
)
