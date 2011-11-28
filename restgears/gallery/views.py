# Create your views here.
import logging
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import View, ModelView
from djangorestframework.mixins import InstanceMixin, ReadModelMixin, DeleteModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin, AuthMixin
from djangorestframework.resources import ModelResource
from djangorestframework.utils import as_tuple
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.views.decorators.cache import never_cache, cache_control 
from filetransfers.api import serve_file, prepare_upload
from djangorestframework import status
from djangorestframework.response import Response, ErrorResponse
from gallery.models import Photo, Vote, Gallery
from google.appengine.ext import blobstore
from django.core.cache import cache
import urllib


log = logging.getLogger(__name__)
class GalleryOverviewView(View):
    """Welcome to the Gallery Module.

    1. index (all galleries)

    """
    permissions = ( IsAuthenticated,)
    
    def get(self, request):
        return [{'name': 'Gallery Categories Index', 'url': reverse('gallery-index')},
                {'name': 'Current User Uploads', 'url': reverse('photos-current-user')},
                ]

class GalleryListView(InstanceMixin, ReadModelMixin, ModelView):
    _suffix = 'Instance'
    permissions = ( IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        instance = super(GalleryListView, self).get(request, *args, **kwargs)
        return instance

class PhotoView(ListModelMixin, DeleteModelMixin, ModelView):
    _suffix = 'Instance'
    permissions = ( IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        photo = super(PhotoView, self).get(request, *args, **kwargs)
        return photo

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
        if instance.can_delete(self.user):
            instance.delete()
        return

class PhotoListView(ListModelMixin, ModelView):
    _suffix = 'List'
    permissions = ( IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        #kwargs['user'] = self.user
        
        if 'user' in kwargs and kwargs['user'] == 'me':
            kwargs['user'] = self.user        
        
        if 'ordering' in request.GET:
            kwargs['ordering']= str(request.GET['ordering'])

        if 'ordering' in kwargs:
            sortkey = kwargs['ordering'] 
            del kwargs['ordering']
            if hasattr(self.resource, 'orderings') and sortkey in self.resource.orderings:
                orderings = self.resource.orderings[sortkey]
                return self.resource.model.objects.order_by(*orderings).filter(**kwargs)
        else:
            return self.resource.model.objects.filter(**kwargs)


class PhotoVoteView(ReadModelMixin, ModelView):
    permissions = ( IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        photo = super(PhotoVoteView, self).get(request, *args, **kwargs)
        if photo.can_vote(self.user):
            vote = Vote(photo=photo, user=self.user)
            vote.save()
            Photo.objects.filter(pk=photo.id).update(votes=F('votes')+1)
            photo.votes+=1 # just, so that the updated object is delivered
        return photo

class PostPhotoUploadView(CreateModelMixin, ModelView):
    permissions = ( IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # translated 'related_field' kwargs into 'related_field_id'

        kwargs.update({'user_id':kwargs['user_id'],
                       'gallery_id':kwargs['pk'],
                       })
        del kwargs['pk']
        all_kw_args = dict(self.CONTENT.items() + kwargs.items())
        log.info("Returning from BlobStore, kwargs: %s, "%(all_kw_args))
        super(PostPhotoUploadView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect("http://google.com")
        #if 'pk' in kwargs:
         #   kwargs.update({'gallery_id':kwargs['pk'],
          #                 'user_id':1,})
           # super(PhotoUploadView, self).post(request, *args, **kwargs)
            #return HttpResponseRedirect("http://google.com")
            
        # redirect to the proper post
    
class PhotoUploadView(View):
    permissions = ( IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        log.debug("in PhotoUploadView.get: args=%s, kwargs=%s"%(args, kwargs))
        target_url = reverse('photo-upload-user', kwargs={'pk':kwargs['pk'],'user_id':self.user.id})
        log.debug("Target URL: %s"%(target_url,))
        upload_url, upload_data = prepare_upload(request, target_url)
        log.debug("Upload URL: %s"%(upload_url,))
        #upload_url = blobstore.create_upload_url(target_url)
        result = {'upload_url':upload_url, 'target_url': target_url}
        log.debug("Result: %s"%(result,))
        return result
#        
#class PhotoDeleteView(DeleteModelMixin, ModelView, View):
#    permissions = ( IsAuthenticated,)
#    def delete(self, request, *args, **kwargs):
#        model = self.resource.model
#        try:
#            if args:
#                # If we have any none kwargs then assume the last represents the primrary key
#                instance = model.objects.get(pk=args[-1], **kwargs)
#            else:
#                # Otherwise assume the kwargs uniquely identify the model
#                instance = model.objects.get(**kwargs)
#        except model.DoesNotExist:
#            raise ErrorResponse(status.HTTP_404_NOT_FOUND, None, {})
#        if instance.user.id == self.user.id:
#            instance.delete()
#        return
#    #def get(self, request, *args, **kwargs):
     #   photo = super(PhotoDeleteView, self).get(request, *args, **kwargs)
      #  if photo.user.id == self.user.id:
       #     photo.delete()
        #    return True
        #else:
         #   return False
        #[{'name': 'Gallery Categories Index', 'url': reverse('gallery-index')},]


class PhotoFlagView(ReadModelMixin, ModelView):
    def get(self, request, *args, **kwargs):
        photo = super(PhotoFlagView, self).get(request, *args, **kwargs)
        photo.flagged = True
        photo.save()
        return photo


