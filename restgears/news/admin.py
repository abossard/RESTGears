from django.contrib import admin
from news.models import Entry, Image
from filetransfers.admin import FiletransferAdmin
from django.forms import FileInput, ClearableFileInput, ModelForm, Textarea
from django.db import models
from django.utils.safestring import mark_safe
from base.fields import AdminImageWidget
from base.admin import BaseModelAdmin

class EntryForm(ModelForm):
    
    class Meta:
        model = Entry
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 20, 'class':'wysiwyg',}),
        }

class EntryAdmin(BaseModelAdmin):
    form = EntryForm
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',
                       )
            }),
            ('Content', {
            'classes': ('wide',),
            'fields': ('teaser','content',)
            }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ( 'publish_on','slug',( 'created_on', 'updated_on',),)
            }),

        )
    class Media:
        js = ('js/jquery.js',
              'jwysiwyg/jquery.wysiwyg.js',
              'jwysiwyg/controls/wysiwyg.link.js',
              'jwysiwyg/controls/wysiwyg.cssWrap.js',
              'jwysiwyg/controls/wysiwyg.table.js',
              'jwysiwyg/controls/wysiwyg.image.js',
              'jwysiwyg/controls/wysiwyg.colorpicker.js',
              'jwysiwyg_start.js',
          )
        css = {'all': (
                       'jwysiwyg/jquery.wysiwyg.css',
                       'css/wysiwyg.css',
                       )}
           
    #formfield_overrides = {
    #    models.TextField: {'widget': AlohaEditorWidget},
    #}

admin.site.register(Entry, EntryAdmin)

class ImageAdmin(FiletransferAdmin):
    fields = ('newsentry','image', 'description','orderindex')
    list_display= ('preview_image','newsentry', 'description',)
    list_filter = ('newsentry',)
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }    

admin.site.register(Image, ImageAdmin)
