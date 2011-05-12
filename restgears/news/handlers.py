from piston.handler import AnonymousBaseHandler
from news.models import Entry

class EntryHandler(AnonymousBaseHandler):
   allowed_methods = ('GET',)
   model = Entry
   fields = ('name', 'teaser', 'content', ('image_set',('image','description',),),'id','slug')
