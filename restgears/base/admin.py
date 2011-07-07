from django.contrib import admin
from django.db import models
from filetransfers.admin import FiletransferAdmin
from fields import BlobFileInput, AdminImageWidget

#from base.models import Category, Taglist, Tag, Image, Imagelist

class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish_on')
    list_display_links = ('name',)
    #list_editable = ('publish_on', )
    list_filter = ('publish_on',)
    search_fields = ['name',]

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',
                       'publish_on',
                       )
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('slug',( 'created_on', 'updated_on',),)
        }),
    )
    #fields = ('name', 'slug', 'teaser', 'content', 'publish_on', 'category', 'taglist', 'created_on', 'updated_on',)
    prepopulated_fields = {"slug": ("name",)}
    #date_hierarchy = 'publish_on'
    exclude = ('deleted_on', )
    readonly_fields = ('created_on', 'updated_on',)



    
#class CategoryAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(Category, CategoryAdmin)
#
#class TaglistAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(Taglist, TaglistAdmin)
#
#
#
#class ImageInline(admin.StackedInline):
#    fields = ('imagedata', 'description',)
#    model = Image
#    formfield_overrides = {
#        models.ImageField: {'widget': AdminImageWidget},
#    }
#    template = 'base/stacked.html'
#
#class ImagelistAdmin(admin.ModelAdmin):
#    inlines = [
#        ImageInline,
#    ]
#
##admin.site.register(Imagelist, ImagelistAdmin)
#
#
#class TagAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(Tag, TagAdmin)
#
#
#class ImageAdmin(FiletransferAdmin):
#    fields = ('imagedata', 'description',)
#    list_display= ('preview_html','description',)
#
##admin.site.register(Image, ImageAdmin)
