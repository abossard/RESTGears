import logging

from django.contrib.auth.backends import ModelBackend
from account.models import DeviceAuthToken, User

class DeviceAuthTokenBackend(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        #find auth token
        log = logging.getLogger(__name__)
        log.debug('Trying device auth login with username=%s and password=%s'%(username, password, ))
        try:
            deviceAuthToken = DeviceAuthToken.objects.get(unique_id=username, token=password)
            log.debug('Token found! Registered on %s with User Agent %s'%(deviceAuthToken.authenticated_on, deviceAuthToken.user_agent))
            if deviceAuthToken.banned:
                log.info('Login denied!')
                return None
            return deviceAuthToken.user
        except DeviceAuthToken.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
