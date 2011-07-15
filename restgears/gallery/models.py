from django.db import models
from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from base.models import BaseModel
from base.utils import reverse
from account.models import User


class Gallery(BaseModel):
    class Meta:
        verbose_name_plural = 'Galleries';


class Photo(models.Model):
    image = models.ImageField(upload_to='uploads/gallery', );
    gallery = models.ForeignKey(Gallery, related_name='photos')
    votes = models.PositiveIntegerField(default=0);
    user = models.ForeignKey(User, related_name='photos')
    uploaded_on =  models.DateTimeField(auto_now_add=True)
    lastvote_on =  models.DateTimeField(auto_now=True)

    def can_vote(self, user):
        return not bool(self.vote_set.filter(user=user))

    def can_delete(self, user):
        return self.user.id == user.id

    def get_absolute_url(self):
        from gallery.views import download_handler
        return reverse(download_handler, kwargs={'pk':self.pk,}) 
    image_url = property(get_absolute_url)

    def preview_image(self):
        return u'<img src="%s" alt="Uploaded on %s by %s" height="100"/>'%(self.image_url, self.uploaded_on, self.user)
    preview_image.allow_tags = True

    class Meta:
        ordering = ['-votes', '-uploaded_on']

class Vote(models.Model):
    user = models.ForeignKey(DjangoUser, related_name='votes')
    photo = models.ForeignKey(Photo, related_name='vote_set')
