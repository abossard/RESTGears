import logging
# Create your views here.
from django.db.models import ImageField, CharField, F
from django.core.urlresolvers import reverse
from djangorestframework.views import View
from djangorestframework.compat import View as DjangoView
from django.http import HttpResponseRedirect
from django.conf import settings
    # Create your views here.
from django.shortcuts import get_object_or_404
from filetransfers.api import serve_file
#from base.models import Image

log = logging.getLogger(__name__)

class Overview(View):
    """This is the Powerfood App Administration System.

    Unauthorized use is strictly prohibited.

    """

    def get(self, request):
        if settings.DEBUG:
            return [{'name': 'News Overview', 'url': reverse('news-overview')},
                {'name': 'Gallery Overview', 'url': reverse('gallery-index')},
                {'name': 'Account Overview', 'url': reverse('account-overview')},
                ]
        else:
            return

#def image_download_handler(request, pk):
#    image = get_object_or_404(Image, pk=pk)
#    return serve_file(request, image.imagedata)

class ImageServeView(DjangoView):

    container = None
    image_field = None
    image_field_type = CharField
    
    def get(self, request, pk=None, max_width=None, max_height=None):
        # find the blobfield/imagefield
        log = logging.getLogger(__name__)
        instance = get_object_or_404(self.container, pk=pk)    
        if not self.image_field:
            for field in self.container._meta.fields:       
                if isinstance(field, ImageField):
                    self.image_field = field.name
                    self.image_field_type = type(field)
                    break
            if not self.image_field:
                raise Exception('No ImageField found')
            
        if hasattr(instance, 'views'):
            self.container.objects.filter(pk=pk).update(views=F('views')+1)
            log.debug('image view: %s Referer: %s'%(instance, request.META.get('HTTP_REFERER', '')))
        field_data = getattr(instance, self.image_field)
        if self.image_field_type == ImageField:
            return serve_file(request, field_data)
        elif self.image_field_type == CharField:
            return HttpResponseRedirect(field_data)
        else:
            raise Exception('Unsupported Image Field')
            
    
    