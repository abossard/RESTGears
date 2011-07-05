from django.contrib import admin
from django.db import models
from filetransfers.admin import FiletransferAdmin
from fields import BlobFileInput, AdminImageWidget

from base.models import Category, Taglist, Tag, Image, Imagelist


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class TaglistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Taglist, TaglistAdmin)



class ImageInline(admin.StackedInline):
    fields = ('imagedata', 'description',)
    model = Image
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }
    template = 'base/stacked.html'

class ImagelistAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]

#admin.site.register(Imagelist, ImagelistAdmin)


class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)


class ImageAdmin(FiletransferAdmin):
    fields = ('imagedata', 'description',)
    list_display= ('preview_html','description',)

#admin.site.register(Image, ImageAdmin)
