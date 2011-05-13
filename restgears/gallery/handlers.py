from piston.handler import AnonymousBaseHandler
from gallery.models import Photo

class PhotoHandler(AnonymousBaseHandler):
   allowed_methods = ('GET',)
   model = Photo
