# Create your views here.
from django.shortcuts import get_object_or_404
from djangorestframework.views import View
from django.core.urlresolvers import reverse
from filetransfers.api import serve_file
from djangorestframework.views import View, ModelView
from djangorestframework.mixins import InstanceMixin, ReadModelMixin, DeleteModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin, AuthMixin

class News(View):
    """Welcome to the News Module.

    1. index (all news)

    Please feel free to browse, create, edit and delete the resources in these examples."""

    def get(self, request):
        return [{
                 'name': 'News Index', 'url': reverse('news-index'),},
                 {'name': 'Article Index', 'url': reverse('article-index'),
                 },]


class ArticleView(ListModelMixin, InstanceMixin, ModelView):
    #_suffix = 'Instance'
    
    def get(self, request, *args, **kwargs):
        article = super(ArticleView, self).get(request, *args, **kwargs)
        return article
    
def download_handler(request, pk):
    from publisher.models import NewsImage
    image = get_object_or_404(NewsImage, pk=pk)
    return serve_file(request, image.image)
