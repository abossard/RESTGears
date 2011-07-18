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

class Gallery(BaseModel):
    class Meta:
        verbose_name_plural = 'Galleries';


class Photo(models.Model):
    image = models.ImageField(upload_to='uploads/gallery', );
    gallery = models.ForeignKey(Gallery, related_name='photos')
    votes = models.PositiveIntegerField(default=0);
    user = models.ForeignKey(User, related_name='photos')
    nickname = models.CharField(editable=False)
    uploaded_on =  models.DateTimeField(auto_now_add=True)
    lastvote_on =  models.DateTimeField(auto_now=True)

    def can_vote(self, user):
        log = logging.getLogger(__name__)
        
        cache_key = 'can_vote-%d-%d'%(self.pk, self.user.id)
        result = cache.add(cache_key, not bool(self.vote_set.filter(user=user)), 2592000)
        log.debug('CanVote Result: %s, executed: %s'%(cache.get(cache_key), result))
        
        return cache.get(cache_key)

    def can_delete(self, user):
        return self.user.id == user.id

    def get_absolute_url(self):
        return reverse('serve-photo', kwargs={'pk':self.pk,}) 
    image_url = property(get_absolute_url)

    def preview_image(self):
        return u'<img src="%s" alt="Uploaded on %s by %s" height="100"/>'%(self.image_url, self.uploaded_on, self.user)
    preview_image.allow_tags = True

    class Meta:
        ordering = ['-votes', '-uploaded_on']

def update_photo(sender, instance, raw, **kwargs):
    if not raw:
        instance.nickname = instance.user.get_profile().nickname

pre_save.connect(update_photo, sender=Photo)

class Vote(models.Model):
    user = models.ForeignKey(DjangoUser, related_name='votes')
    photo = models.ForeignKey(Photo, related_name='vote_set')
    
def update_vote_cache(sender, instance, created, **kwargs):
    log = logging.getLogger(__name__)
    cache_key = 'can_vote-%d-%d'%(instance.photo.id, instance.user.id)
    if created:
        cache.set(cache_key, False, 2592000)        
        log.debug('Updating cache "%s" to %s'%(cache_key, cache.get(cache_key),))


post_save.connect(update_vote_cache, sender=Vote)
    