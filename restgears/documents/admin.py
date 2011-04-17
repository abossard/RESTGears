from django.contrib import admin
from restgears.documents.models import Document, Category, Tag

class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Document, DocumentAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
