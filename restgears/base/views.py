# Create your views here.
from django.db.models import ImageField
from django.core.urlresolvers import reverse
from djangorestframework.views import View
from djangorestframework.compat import View as DjangoView
    # Create your views here.
from django.shortcuts import get_object_or_404
from filetransfers.api import serve_file
#from base.models import Image


class Overview(View):
    """This is the Powerfood App Administration System.

    Unauthorized use is strictly prohibited.

    """

    def get(self, request):
        return [{'name': 'News Overview', 'url': reverse('news-overview')},
                {'name': 'Gallery Overview', 'url': reverse('gallery-index')},
                {'name': 'Account Overview', 'url': reverse('account-overview')},
                ]

#def image_download_handler(request, pk):
#    image = get_object_or_404(Image, pk=pk)
#    return serve_file(request, image.imagedata)

class ImageServeView(DjangoView):

    container = None
    image_field = None
    
    def get(self, request, pk=None):
        # find the blobfield/imagefield
        if not self.image_field:
            for field in self.container._meta.fields:       
                if isinstance(field, ImageField):
                    self.image_field = field.name
                    break
            if not self.image_field:
                raise Exception('No ImageField found')        
        image = get_object_or_404(self.container, pk=pk)
        
        return serve_file(request, getattr(image, self.image_field),)
    
    