# Create your views here.
from django.core.urlresolvers import reverse
from djangorestframework.views import View
    # Create your views here.
from django.shortcuts import get_object_or_404
from filetransfers.api import serve_file
#from base.models import Image


class Overview(View):
    """Welcome to RESTGears. Made with [Django REST framework](http://django-rest-framework.org).

    RESTGears is a generic approach in providing a backend, that runs on various platforms and supports some generic functionality.

    All the example APIs allow anonymous access, and can be navigated either through the browser or from the command line...

        bash: curl -X GET http://somedomain.com/                           # (Use default renderer)
        bash: curl -X GET http://somedomain.com/ -H 'Accept: text/plain'   # (Use plaintext documentation renderer)

    The modules provided: 
   
    1. A news module

    Please feel free to browse, create, edit and delete the resources in these examples."""

    def get(self, request):
        return [{'name': 'News Overview', 'url': reverse('news-overview')},
                {'name': 'Gallery Overview', 'url': reverse('gallery-overview')},
                {'name': 'Account Overview', 'url': reverse('account-overview')},
                ]

#def image_download_handler(request, pk):
#    image = get_object_or_404(Image, pk=pk)
#    return serve_file(request, image.imagedata)

