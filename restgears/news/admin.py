from django.contrib import admin
from news.models import Entry, Image
from filetransfers.admin import FiletransferAdmin

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

class ImageAdmin(FiletransferAdmin):
    pass
admin.site.register(Image, ImageAdmin)



