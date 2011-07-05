from django.db import models
from django.utils.safestring import mark_safe
from django.forms import FileInput, ClearableFileInput
from base.utils import reverse


class BlobFileInput(FileInput):
    def render(self, name, value, attrs=None):
        #for attr in dir(value):
        #    print "obj.%s = %s" % (attr, getattr(value, attr))
        return super(FileInput, self).render(name, None, attrs=attrs) + mark_safe(
            u'Blob with Name: %s, Size %s Bytes' %(value.file, value.size) if hasattr(value,'file') else  'NO'
            )
    
    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        print 'value from datadic'
        return files.get(name, None)

    def _has_changed(self, initial, data):
        print 'has changed'
        if data is None:
            return False
        return True

class AdminImageWidget(FileInput):

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "file"):
            output.append('Filename: %s, Size: %s<br/>'
                          '' 
                           % (value.file.name, value.file.size))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
