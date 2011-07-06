from django.db import models
from django.conf import settings
from base.models import BaseModel
from base.utils import reverse
from django.contrib.auth.models import User

class Gallery(BaseModel):
    def get_absolute_url(self):
        return reverse('gallery-instance', kwargs={'pk':self.pk,})
    
    url = property(get_absolute_url)

    class Meta:
        verbose_name_plural = 'Galleries';


class Photo(models.Model):
    image = models.ImageField(upload_to='uploads/gallery');
    gallery = models.ForeignKey(Gallery, related_name='photos')
    votes = models.PositiveIntegerField(default=0);
    user = models.ForeignKey(User, related_name='photos')
    uploaded_on =  models.DateTimeField(auto_now_add=True)
    lastvote_on =  models.DateTimeField(auto_now=True)
    def can_vote(self, user):
        return not bool(self.vote_set.filter(user=user))
    
    def get_absolute_url(self):
        from gallery.views import download_handler
        return reverse(download_handler, kwargs={'pk':self.pk,}) 
    image_url = property(get_absolute_url)

    def _url(self):
        return reverse('photo-instance', kwargs={'pk':self.pk,}) 
    url = property(_url)
    
    def get_photo_vote_url(self):
        return reverse('photo-vote', kwargs={'pk':self.pk,})
    
    vote_url = property(get_photo_vote_url)

    def get_photo_delete_url(self):
        return reverse('photo-delete', kwargs={'pk':self.pk,})
    
    delete_url = property(get_photo_delete_url)
    
    def preview_image(self):
        return u'<img src="%s" alt="Uploaded on %s by %s" height="100"/>'%(self.image_url, self.uploaded_on, self.user)
    preview_image.allow_tags = True

class Vote(models.Model):
    user = models.ForeignKey(User, related_name='votes')
    photo = models.ForeignKey(Photo, related_name='vote_set')
