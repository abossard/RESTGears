from django.contrib import admin
from news.models import Entry, Image
from filetransfers.admin import FiletransferAdmin
from django.forms import FileInput, ClearableFileInput
from django.db import models
from django.utils.safestring import mark_safe
from base.fields import AdminImageWidget
from base.admin import BaseModelAdmin


class EntryAdmin(BaseModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',
                       'publish_on',
                       )
            }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('site', 'slug',( 'created_on', 'updated_on',),)
            }),
        ('Content', {
            'classes': ('wide',),
            'fields': ('teaser','content',)
            }),
        )

admin.site.register(Entry, EntryAdmin)

class ImageAdmin(FiletransferAdmin):
    fields = ('newsentry','image', 'description',)
    list_display= ('preview_image','newsentry', 'description',)
    list_filter = ('newsentry',)
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }    

admin.site.register(Image, ImageAdmin)
