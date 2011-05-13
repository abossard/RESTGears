from piston.handler import BaseHandler

class CsrfExemptBaseHandler(BaseHandler):
    """
    handles request that have had csrfmiddlewaretoken inserted 
    automatically by django's CsrfViewMiddleware
    """
    def flatten_dict(self, dct):
        print dct
        if 'csrfmiddlewaretoken' in dct:
            # dct is a QueryDict and immutable
            dct = dct.copy()  
            del dct['csrfmiddlewaretoken']
        return super(CsrfExemptBaseHandler, self).flatten_dict(dct)
