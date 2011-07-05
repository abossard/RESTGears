# Create your views here.
from django.core.urlresolvers import reverse
from djangorestframework.views import View
    # Create your views here.
from django.shortcuts import get_object_or_404
from filetransfers.api import serve_file
from base.models import Image


class Overview(View):
    """Welcome to RESTGears. Made with [Django REST framework](http://django-rest-framework.org).

    RESTGears is a generic approach in providing a backend, that runs on various platforms and supports some generic functionality.

    All the example APIs allow anonymous access, and can be navigated either through the browser or from the command line...

        bash: curl -X GET http://api.django-rest-framework.org/                           # (Use default renderer)
        bash: curl -X GET http://api.django-rest-framework.org/ -H 'Accept: text/plain'   # (Use plaintext documentation renderer)

    The modules provided: 
   
    1. A basic example using the [Resource](http://django-rest-framework.org/library/resource.html) class.

    Please feel free to browse, create, edit and delete the resources in these examples."""

    def get(self, request):
        return [{'name': 'News Index', 'url': reverse('news-index')},]



def image_download_handler(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return serve_file(request, image.imagedata)

