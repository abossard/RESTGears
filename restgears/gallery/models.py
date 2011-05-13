from django.db import models
from django.conf import settings
from restgears.base.models import BaseModel

class Photo(BaseModel):
    image = models.FileField(upload_to='uploads/gallery');
    def _url(self):
        return settings.MEDIA_URL + str(self.image);
    url = property(_url)
    
