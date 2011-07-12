from django.db import models
from django.contrib.auth.models import User
# Create your models here.


#class User(BaseUser):
#    class Meta:
#        proxy = True

class DeviceAuthToken(models.Model):
    user = models.ForeignKey(User, related_name='auth_tokens')
    unique_id = models.CharField(max_length=255)
    ip_address = models.IPAddressField()
    authenticated_on = models.DateTimeField(auto_now_add=True)
