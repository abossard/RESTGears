try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

DEFAULT_SITE_ID = 1

_thread_locals = local()

def get_current_site():
    return getattr(_thread_locals, 'SITE_ID', 1)

def set_current_site_id(site):
    setattr(_thread_locals, 'SITE_ID', site)

        
class SiteIDHook(object):
    def __repr__(self):
        return str(self.__int__())

    def __int__(self):
        return get_current_site_id()

    def __hash__(self):
        return self.__int__()

    def set(self, value):
        set_current_site_id(value)
