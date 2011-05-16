# Create your views here.
from piston.doc import generate_doc

from django.http import HttpResponse

def doc(request, handler=None):
    documentation = generate_doc(handler)
    html = "<html><body>It is now %s.</body></html>" % documentation.resource_uri_template
    return HttpResponse(html)
