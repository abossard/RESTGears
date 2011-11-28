import logging
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from django.core.cache import cache
from base.models import BaseModel
from base.utils import reverse
from account.models import User
from base.utils import cacheable, stales_cache
from google.appengine.api import images

class Gallery(BaseModel):
    class Meta:
        verbose_name_plural = 'Galleries';


class Photo(models.Model):
    image = models.ImageField(upload_to='uploads/gallery', );
    gallery = models.ForeignKey(Gallery, related_name='photos')
    rank = models.IntegerField(editable=False, default=0)
    votes = models.PositiveIntegerField(default=0);
    views = models.PositiveIntegerField(default=0);
    user = models.ForeignKey(User, related_name='photos')
    nickname = models.CharField(editable=False, max_length=128)
    flagged = models.BooleanField(default=False)
    uploaded_on =  models.DateTimeField(auto_now_add=True)
    lastvote_on =  models.DateTimeField(auto_now=True)

    def can_vote(self, user):
        log = logging.getLogger(__name__)
        
        cache_key = 'can_vote-%d-%d'%(self.pk, user.id)
        result = cache.get(cache_key)
        if result is None:
            result = not bool(self.vote_set.filter(user=user))
            cache.set(cache_key, result, 875000)
            log.debug('CanVote Result: %s, executed: %s'%(cache.get(cache_key), result))
        #result = cache.add(cache_key,not bool(self.vote_set.filter(user=user)) , 2592000)
        return result

    def can_delete(self, user):
        return self.user_id == user.id

    def get_absolute_url(self):
        return reverse('photo-instance', kwargs={'pk':self.pk,}) 
    
    #def get_image_url(self):
    #    return self._get_serving_url()
    image_url = models.CharField(editable=False, max_length=255)

    #def get_thumb_image_url(self):
    #    return self._get_serving_url(100)
    thumb_image_url = models.CharField(editable=False, max_length=255)
    
    def _get_serving_url(self, size=None):
        blob_key = str(self.image.file.blobstore_info.key()) 
        thumbnail_picture_url =  images.get_serving_url(blob_key) if size is None else images.get_serving_url(blob_key, size)
        return thumbnail_picture_url

    def preview_image(self):
        return u'<img src="%s" alt="Uploaded on %s by %s" height="100"/>'%(self.thumb_image_url, self.uploaded_on, self.user)
    preview_image.allow_tags = True

    class Meta:
        ordering = ['-votes','-views', '-uploaded_on']

def update_photo(sender, instance, raw, **kwargs):
    if not raw:
        instance.nickname = instance.user.get_profile().nickname

pre_save.connect(update_photo, sender=Photo)

def create_photo(sender, instance, created, **kwargs):
    if created:
        blob_key = str(instance.image.file.blobstore_info.key()) 
        instance.image_url = images.get_serving_url(blob_key, 960)
        instance.thumb_image_url = images.get_serving_url(blob_key,100)
        instance.save()
post_save.connect(create_photo, sender=Photo)

class Vote(models.Model):
    user = models.ForeignKey(DjangoUser, related_name='votes')
    photo = models.ForeignKey(Photo, related_name='vote_set')
    
def update_vote_cache(sender, instance, created, **kwargs):
    log = logging.getLogger(__name__)
    cache_key = 'can_vote-%d-%d'%(instance.photo.id, instance.user.id)
    if created:
        cache.set(cache_key, False, 875000)        
        log.debug('Updating cache "%s" to %s'%(cache_key, cache.get(cache_key),))

post_save.connect(update_vote_cache, sender=Vote)
    