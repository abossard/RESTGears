# Create your views here.
import logging

from djangorestframework.views import View, ModelView
from djangorestframework.mixins import InstanceMixin, ReadModelMixin, DeleteModelMixin, UpdateModelMixin, CreateModelMixin, AuthMixin
from djangorestframework.resources import ModelResource
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from filetransfers.api import serve_file, prepare_upload
from djangorestframework import status
from djangorestframework.response import Response, ErrorResponse
from gallery.models import Photo, Vote
import urllib
from google.appengine.api import urlfetch


class GalleryOverviewView(View):
    """Welcome to the Gallery Module.

    1. index (all galleries)

    Please feel free to browse, create, edit and delete the resources in these examples."""

    def get(self, request):
        return [{'name': 'Gallery Categories Index', 'url': reverse('gallery-index')},]

class GalleryListView(InstanceMixin, ReadModelMixin, ModelView):
    _suffix = 'Instance'
    def get(self, request, *args, **kwargs):
        instance = super(GalleryListView, self).get(request, *args, **kwargs)
        return instance

class PhotoView(ReadModelMixin, ModelView):
    _suffix = 'Instance'
    def get(self, request, *args, **kwargs):
        photo = super(PhotoView, self).get(request, *args, **kwargs)
        self.resource.fields = self.resource.base_fields
        if photo.can_vote(self.user):
            self.resource.fields = self.resource.fields + self.resource.vote_field
        if photo.user.id == self.user.id:
            self.resource.fields = self.resource.fields + self.resource.delete_field
        return photo

class PhotoVoteView(ReadModelMixin, ModelView):
    def get(self, request, *args, **kwargs):
        photo = super(PhotoVoteView, self).get(request, *args, **kwargs)
        if photo.can_vote(self.user):
            vote = Vote(photo=photo, user=self.user)
            vote.save()
            photo.votes+=1
            photo.save()
        return HttpResponseRedirect(photo.url)
        
class PhotoUploadView(CreateModelMixin, ModelView):
    def get(self, request, *args, **kwargs):
        target_url = reverse('photo-upload-user', kwargs={'pk':kwargs['pk'],'user_id':self.user.id})
        upload_url, upload_data = prepare_upload(request, target_url)
        return {'upload_url':upload_url, 'curl_example':'curl %s -X POST -F image=@image01.jpg'%(upload_url,)}
        
    def post(self, request, *args, **kwargs):
        # translated 'related_field' kwargs into 'related_field_id'
        kwargs.update({'user_id':kwargs['user_id'],
                       'gallery_id':kwargs['pk'],
                       })
        del kwargs['pk']
        all_kw_args = dict(self.CONTENT.items() + kwargs.items())
        logger = logging.getLogger(__name__)
        logger.error("Returning from BlobStore, kwargs: %s, "%(all_kw_args))
        super(PhotoUploadView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect("http://google.com")
        #if 'pk' in kwargs:
         #   kwargs.update({'gallery_id':kwargs['pk'],
          #                 'user_id':1,})
           # super(PhotoUploadView, self).post(request, *args, **kwargs)
            #return HttpResponseRedirect("http://google.com")
            
        # redirect to the proper post



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
