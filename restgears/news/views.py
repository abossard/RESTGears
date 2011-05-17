# Create your views here.
from django.shortcuts import get_object_or_404

from filetransfers.api import serve_file
from news.models import Image

def download_handler(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return serve_file(request, image.image)
