from django.db import models
from django.conf import settings
from restgears.base.models import BaseModel

class Entry(BaseModel):
    teaser = models.TextField(max_length=500, help_text='Insert text only');
    content = models.TextField(max_length=4000, help_text='Insert HTML here');

    class Meta:
        verbose_name_plural = 'Entries';

class Image(models.Model):
    description = models.TextField(max_length=500, help_text='Insert text only');
    newsentry = models.ForeignKey(Entry, related_name='images');
    image = models.FileField(upload_to='uploads/news');
    def _url(self):
        return settings.MEDIA_URL + str(self.image);
    url = property(_url)    

