from django.db import models
from datetime import datetime


class Document(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text='Choose a name that describes this document')
    type = models.CharField(max_length=100, blank=True, help_text='Use type to better distinguish between documents')
    slug = models.SlugField(max_length=50, db_index=True)
    publish_on = models.DateTimeField(blank=True, null=True, default=datetime.now)
    deleted_on = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def _is_published(self):
        return self.published_on < datetime.now()
    is_published = property(_is_published)

    def _is_deleted(self):
        return self.deleted_on < datetime.now()
    is_deleted = property(_is_deleted)

    def _is_active(self):
        return self.is_published() and not self.is_deleted()
    is_active = property(_is_active)

    def __unicode__(self):
        if (self.type):
            return '%s (%s)' % (self.name, self.type,)
        else:
            return self.name

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('documents.views.show', [str(self.id)])

