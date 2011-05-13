from piston.handler import AnonymousBaseHandler
from gallery.models import Photo

class PhotoHandler(AnonymousBaseHandler):
   allowed_methods = ('GET','POST',)
   fields = ('name',
             'teaser',
             'content',
             'url',
             'slug',
             'publish_on',
             ('category', ('name',),),
             ('taglist',(('tags',('name',),),),),
   )

   model = Photo
