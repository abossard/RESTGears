from django.db import models
from dbindexer.api import register_index
from django.contrib.auth.models import User as BaseUser
from django.db.models.signals import post_save

# Create your models here.


class User(BaseUser):

    # these fields are just here, so it doesnt crash that hard
    # please don't ask me why it works with them :-(
    idxf_username_l_iexact = None
    idxf_email_l_iexact = None
    
    class Meta:
        proxy = True

class DeviceAuthToken(models.Model):
    user = models.ForeignKey(BaseUser, related_name='auth_tokens')
    unique_id = models.CharField(max_length=255, unique=True, )
    user_agent = models.CharField(max_length=255, )
    ip_address = models.IPAddressField()
    token = models.CharField(max_length=255, )
    authenticated_on = models.DateTimeField(auto_now_add=True)
    banned = models.BooleanField(default=False, help_text='Disable this Login Token to prevent the Client with the specified unique id from logging in.', verbose_name='Banned')

    def __unicode__(self):
        return 'DeviceAuthToken %s (User %s on %s)'%(self.unique_id, self.user.username, self.authenticated_on)

    class Meta:
        ordering = ['-authenticated_on']

  
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(BaseUser)

    # Other fields here
    nickname = models.CharField(max_length=128)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=BaseUser)
