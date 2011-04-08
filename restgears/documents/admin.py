from django.contrib import admin
from restgears.documents.models import Document

class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Document, DocumentAdmin)
