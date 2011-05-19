from django.contrib import admin
from news.models import Entry, Image
from filetransfers.admin import FiletransferAdmin
from django.forms import FileInput, ClearableFileInput
from django.db import models
from django.utils.safestring import mark_safe
import pprint

class ImageInline(admin.StackedInline):
    fields = ('image', 'description',)
    model = Image

class EntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish_on')
    list_display_links = ('name',)
    #list_editable = ('publish_on', )
    list_filter = ('publish_on',)
    search_fields = ['name',]

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'teaser', 'content', 'publish_on', )
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('site', 'slug','category', 'taglist',( 'created_on', 'updated_on',),)
        }),
    )
    #fields = ('name', 'slug', 'teaser', 'content', 'publish_on', 'category', 'taglist', 'created_on', 'updated_on',)
    prepopulated_fields = {"slug": ("name",)}
    #date_hierarchy = 'publish_on'
    exclude = ('deleted_on', )
    readonly_fields = ('created_on', 'updated_on',)
    inlines = [
        ImageInline,
    ]


admin.site.register(Entry, EntryAdmin)

class BlobFileInput(FileInput):
    def render(self, name, value, attrs=None):
        #for attr in dir(value):
        #    print "obj.%s = %s" % (attr, getattr(value, attr))
        return super(FileInput, self).render(name, None, attrs=attrs) + mark_safe(u'<a href="%s">%s</a>'%('a',value.file,))
    
    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        print 'value from datadic'
        return files.get(name, None)

    def _has_changed(self, initial, data):
        print 'has changed'
        if data is None:
            return False
        return True

class ImageAdmin(FiletransferAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': BlobFileInput},
    }

admin.site.register(Image, ImageAdmin)




