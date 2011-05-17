from django.contrib import admin
from base.models import Category, Taglist, Tag


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class TaglistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Taglist, TaglistAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)
