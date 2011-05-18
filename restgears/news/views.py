# Create your views here.
from django.shortcuts import get_object_or_404
from filetransfers.api import serve_file


def download_handler(request, pk):
    from news.models import Image
    image = get_object_or_404(Image, pk=pk)
    return serve_file(request, image.image)
