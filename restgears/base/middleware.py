import logging
import quopri
log = logging.getLogger(__name__)

class BlobRedirectFixMiddleware(object):
    def process_request(self, request):
        if request.method == 'POST' and 'HTTP_X_APPENGINE_BLOBUPLOAD' in request.META and request.META['HTTP_X_APPENGINE_BLOBUPLOAD'] == 'true':
            request.POST = request.POST.copy()
            log.info('POST before decoding: %s' % request.POST)
            for key in request.POST:
                if key.startswith('_') or key == u'csrfmiddlewaretoken':
                    continue
                value = request.POST[key]
                if isinstance(value,(str, unicode)):
                    request.POST[key] = unicode(quopri.decodestring(value), 'iso_8859-2')
            log.info('POST after decoding: %s' % request.POST) 
        return None

    def process_response(self, request, response):
        log.info('REPOSNE Content: %s' % response['Content-type'])
        return response