from django.db import models
from django.conf import settings
from base.utils import reverse

from base.models import BaseModel
from news.views import download_handler

class Entry(BaseModel):
    teaser = models.TextField(max_length=500, help_text='Insert text only');
    content = models.TextField(max_length=4000, help_text='Insert HTML here');
    class Meta:
        verbose_name_plural = 'News Entries';

  
class Image(models.Model):
    description = models.TextField(max_length=500, help_text='Insert text only', blank=True);
    newsentry = models.ForeignKey(Entry, related_name='images');
    image = models.ImageField(upload_to='uploads/news');

    def get_absolute_url(self):
        return reverse(download_handler, kwargs={'pk':self.pk,}) 
    url = property(get_absolute_url)

    def preview_image(self):
        return u'<img src="%s" alt="%s" height="100"/>'%(self.url, self.description)
    
    preview_image.allow_tags = True

    class Meta:
        verbose_name_plural = 'News Images';
