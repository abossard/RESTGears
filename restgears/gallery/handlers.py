#from base.handler import CsrfExemptBaseHandler
from piston.handler import BaseHandler, AnonymousBaseHandler
from gallery.models import Photo
from gallery.forms import PhotoForm

class PhotoHandler(BaseHandler):
   anonymous = 'AnonymousPhotoHandler'

   allowed_methods = ('GET','POST',)
   fields = ('name',
             'url',
             'slug',
             'publish_on',
             ('category', ('name',),),
             ('taglist',(('tags',('name',),),),),
   )
   model = Photo
   
   def read(self, request, title=None):
      base = Photo.objects
      return base.all()

   def create(self, request):
      form = PhotoForm(request.POST, request.FILES)
      print form
      if form.is_valid():
         print request.FILES['image']
         new_photo = form.save()
         return new_photo
      else:
         return form.errors
      

class AnonymousPhotoHandler(PhotoHandler, AnonymousBaseHandler):
    """
    Anonymous entrypoint for blogposts.
    """
    fields = ('name', 'url',)
