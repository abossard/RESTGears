# Create your views here.
from djangorestframework.views import View, ModelView
from djangorestframework.mixins import InstanceMixin, ReadModelMixin, DeleteModelMixin, UpdateModelMixin, CreateModelMixin
from djangorestframework.resources import ModelResource
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from filetransfers.api import serve_file
from djangorestframework import status
from djangorestframework.response import Response, ErrorResponse
from gallery.models import Photo, Vote

class GalleryOverviewView(View):
    """Welcome to the Gallery Module.

    1. index (all galleries)

    Please feel free to browse, create, edit and delete the resources in these examples."""

    def get(self, request):
        return [{'name': 'Gallery Categories Index', 'url': reverse('gallery-index')},]

class GalleryListView(InstanceMixin, ReadModelMixin, ModelView, View):
    _suffix = 'Instance'
    def get(self, request, *args, **kwargs):
        instance = super(GalleryListView, self).get(request, *args, **kwargs)
        return instance

class PhotoView(ReadModelMixin, ModelView, View):
    _suffix = 'Instance'
    def get(self, request, *args, **kwargs):
        photo = super(PhotoView, self).get(request, *args, **kwargs)
        self.resource.fields = self.resource.base_fields
        if photo.can_vote(self.user):
            self.resource.fields = self.resource.fields + self.resource.vote_field
        if photo.user.id == self.user.id:
            self.resource.fields = self.resource.fields + self.resource.delete_field
        return photo

class PhotoVoteView(ReadModelMixin, ModelView, View):
    def get(self, request, *args, **kwargs):
        photo = super(PhotoVoteView, self).get(request, *args, **kwargs)
        if photo.can_vote(self.user):
            vote = Vote(photo=photo, user=self.user)
            vote.save()
            photo.votes+=1
            photo.save()
        return HttpResponseRedirect(photo.url)
        
class PhotoUploadView(UpdateModelMixin, ModelView, View):
    pass

class PhotoDeleteView(DeleteModelMixin, ModelView, View):
    def delete(self, request, *args, **kwargs):
        model = self.resource.model
        try:
            if args:
                # If we have any none kwargs then assume the last represents the primrary key
                instance = model.objects.get(pk=args[-1], **kwargs)
            else:
                # Otherwise assume the kwargs uniquely identify the model
                instance = model.objects.get(**kwargs)
        except model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND, None, {})
        if instance.user.id == self.user.id:
            instance.delete()
        return
    #def get(self, request, *args, **kwargs):
     #   photo = super(PhotoDeleteView, self).get(request, *args, **kwargs)
      #  if photo.user.id == self.user.id:
       #     photo.delete()
        #    return True
        #else:
         #   return False
        #[{'name': 'Gallery Categories Index', 'url': reverse('gallery-index')},]


def download_handler(request, pk):
    from gallery.models import Photo
    photo = get_object_or_404(Photo, pk=pk)
    return serve_file(request, photo.image)
