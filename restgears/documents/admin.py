from django.contrib import admin
<<<<<<< HEAD
from restgears.documents.models import Document, Category, Tag
=======
from restgears.documents.models import Document, Category
>>>>>>> 3eba3c9fb2fb510c0733cf885cf9a66f99da3fb5

class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Document, DocumentAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
<<<<<<< HEAD

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
=======
>>>>>>> 3eba3c9fb2fb510c0733cf885cf9a66f99da3fb5
