from django.conf import settings
from django.contrib.sites.models import Site
from restgears.base import sites

class SiteSettings(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        if True:
            default_site_id = request.GET.get('site_id', sites.DEFAULT_SITE_ID)
        else:
            default_site_id = sites.DEFAULT_SITE_ID
            
        try:
            current_site_id = Site.objects.get(domain__iexact=request.META["HTTP_HOST"])
        except:
            current_site_id = Site.objects.get(id=default_site_id)
        sites.set_current_site_id(current_site_id.id)
