from django.db import models
from datetime import datetime
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


class BaseModel(models.Model):
    name = models.CharField(max_length=200, help_text='Choose a name that describes this object')
    slug = models.SlugField(max_length=50, db_index=True, help_text='Define a string, that is url conform')
    publish_on = models.DateTimeField(blank=True, null=True, default=datetime.now, help_text='Set the date when this item has to be published')
    deleted_on = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', help_text='Choose a matching category')
    taglist = models.ForeignKey('Taglist')
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def _is_published(self):
        return self.publish_on < datetime.now()
    is_published = property(_is_published)

    def _is_deleted(self):
        return self.deleted_on < datetime.now()
    is_deleted = property(_is_deleted)

    def _is_active(self):
        return self.is_published() and not self.is_deleted()
    is_active = property(_is_active)

    def __unicode__(self):
        return self.name

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('documents.views.show', [str(self.id)])
    class Meta:
        abstract = True
        ordering = ['-created_on']

class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Choose a name that describes this category', db_index=True, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Taglist(models.Model):
    pass

class Tag(models.Model):
    name = models.CharField(max_length=32)
    on_taglist = models.ForeignKey(Taglist, related_name='tags')
    def __unicode__(self):
        return self.name
    
