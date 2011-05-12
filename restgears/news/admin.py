from django.contrib import admin
from restgears.news.models import NewsEntry, Category, Tag

class NewsEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(NewsEntry, NewsEntryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
