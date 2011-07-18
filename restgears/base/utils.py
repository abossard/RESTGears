from django.core import urlresolvers
from django.core.cache import cache

class lazy_string(object):
    def __init__(self, function, *args, **kwargs):
        self.function=function
        self.args=args
        self.kwargs=kwargs
        
    def __str__(self):
        if not hasattr(self, 'str'):
            self.str=self.function(*self.args, **self.kwargs)
        return self.str
    
    def startswith(self, s):
        return str(self).startswith(s)

def reverse(*args, **kwargs):
    return lazy_string(urlresolvers.reverse, *args, **kwargs)


def cacheable(cache_key, timeout=3600):
    def paramed_decorator(func):
        def decorated(self):
            key = cache_key % self.__dict__
            res = cache.get(key)
            if res == None:
                res = func(self)
                cache.set(key, res, timeout)
            return res
        decorated.__doc__ = func.__doc__
        decorated.__dict__ = func.__dict__
        return decorated 
    return paramed_decorator

def stales_cache(cache_key):
    def paramed_decorator(func):
        def decorated(self, *args, **kw):
            key = cache_key % self.__dict__
            cache.delete(key)
            return func(self, *args, **kw)
        decorated.__doc__ = func.__doc__
        decorated.__dict__ = func.__dict__
        return decorated
    return paramed_decorator