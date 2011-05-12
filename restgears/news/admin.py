from django.contrib import admin
from restgears.news.models import Entry, Image, Category, Tag

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Entry, EntryAdmin)

class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
