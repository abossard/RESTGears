from django.contrib import admin
from restgears.news.models import Entry, Image

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Entry, EntryAdmin)

class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)



