from django.contrib import admin
from gallery.models import Photo, Gallery
from base.admin import BaseModelAdmin
from filetransfers.admin import FiletransferAdmin
from base.fields import AdminImageWidget
from django.db import models

class GalleryAdmin(BaseModelAdmin):
    pass

admin.site.register(Gallery, GalleryAdmin)


class PhotoAdmin(FiletransferAdmin):
    fields = ('gallery','image', 'user', 'votes')
    #search_fields = ['user',]
    list_filter = ('gallery',)
    list_display= ('preview_image','gallery', 'user','uploaded_on')
    readonly_fields = ('uploaded_on', 'lastvote_on',)
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

admin.site.register(Photo, PhotoAdmin)
