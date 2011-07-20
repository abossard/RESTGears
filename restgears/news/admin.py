from django.contrib import admin
from news.models import Entry, Image
from filetransfers.admin import FiletransferAdmin
from django.forms import FileInput, ClearableFileInput, ModelForm, Textarea
from django.db import models
from django.utils.safestring import mark_safe
from base.fields import AdminImageWidget
from base.admin import BaseModelAdmin
from base.widgets import AlohaEditorWidget

class EntryForm(ModelForm):
    
    class Meta:
        model = Entry
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 20, 'class':'article wysiwyg',}),
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
        js = ('aloha/aloha.js',
              'aloha/plugins/com.gentics.aloha.plugins.Format/plugin.js',
              'aloha/plugins/com.gentics.aloha.plugins.Table/plugin.js',
              'aloha/plugins/com.gentics.aloha.plugins.List/plugin.js',
              'aloha/plugins/com.gentics.aloha.plugins.Link/plugin.js',
              #'aloha/plugins/com.gentics.aloha.plugins.HighlightEditables/plugin.js',
              'aloha/plugins/com.gentics.aloha.plugins.TOC/plugin.js',
              'aloha/plugins/com.gentics.aloha.plugins.Link/delicious.js',
              'aloha/plugins/com.gentics.aloha.plugins.Link/LinkList.js',
              'aloha/plugins/com.gentics.aloha.plugins.Paste/plugin.js',
              'aloha/plugins/com.gentics.aloha.plugins.Paste/wordpastehandler.js',
              'aloha_settings.js',
              'aloha_start.js',
          )
        css = {'all': ('css/aloha.css',)}
           
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
