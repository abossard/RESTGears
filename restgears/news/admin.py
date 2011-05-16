from django.contrib import admin
from restgears.news.models import Entry, Image

class EntryAdmin(admin.ModelAdmin):
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
    date_hierarchy = 'publish_on'
    exclude = ('deleted_on', )
    readonly_fields = ('created_on', 'updated_on',)

admin.site.register(Entry, EntryAdmin)

class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)



