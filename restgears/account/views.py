import logging

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from djangorestframework.views import View, ModelView
from djangorestframework.mixins import InstanceMixin, ReadModelMixin, DeleteModelMixin, UpdateModelMixin, CreateModelMixin, AuthMixin

from account.models import DeviceAuthToken

class AccountOverviewView(View):
    """Welcome to the Account Module.

    """
    def get(self, request):
        return [{'name': 'Account Retrieve Credentials', 'url': reverse('account-retrieve-credentials')},]

class RetrieveCredentialsView(ModelView):
    def post(self, request, *args, **kwargs):
        log = logging.getLogger(__name__)
        all_kw_args = dict(self.CONTENT.items() + kwargs.items())

        
        log.debug('Request=%s, all_kw_args=%s'%(request, all_kw_args, ))
        nickname = all_kw_args['nickname']
        del all_kw_args['nickname']
        email = all_kw_args['email'].lower()
        del all_kw_args['email']
        all_kw_args['ip_address'] = request.META['REMOTE_ADDR']
        all_kw_args['user_agent'] = request.META['HTTP_USER_AGENT']

        try:
            user = User.objects.get(username=email, email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email, email=email)
        profile = user.get_profile()
        profile.nickname = nickname
        profile.save()
        all_kw_args['user'] = user
        deviceAuthToken, created = DeviceAuthToken.objects.get_or_create(defaults={'token':User.objects.make_random_password() }, **all_kw_args)
        log.debug('User=%s, DeviceAuthToken=%s, Created=%s'%(user, deviceAuthToken, created,))
        
        #kwargs.update({'user_id':kwargs['user_id'],
        #               'gallery_id':kwargs['pk'],
        #               })
        #del kwargs['pk']
        #all_kw_args = dict(self.CONTENT.items() + kwargs.items())
        #logger = logging.getLogger(__name__)
        #logger.info("Returning from BlobStore, kwargs: %s, "%(all_kw_args))
        return {'username':deviceAuthToken.unique_id,
                'password':deviceAuthToken.token,
                'created':created,},
