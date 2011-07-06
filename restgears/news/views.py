# Create your views here.
from django.shortcuts import get_object_or_404
from djangorestframework.views import View
from django.core.urlresolvers import reverse
from filetransfers.api import serve_file

class News(View):
    """Welcome to the News Module.

    1. index (all news)

    Please feel free to browse, create, edit and delete the resources in these examples."""

    def get(self, request):
        return [{'name': 'News Index', 'url': reverse('news-index')},]



def download_handler(request, pk):
    from news.models import Image
    image = get_object_or_404(Image, pk=pk)
    return serve_file(request, image.image)
