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

        if 'nickname' in all_kw_args:
            nickname = all_kw_args['nickname']
            del all_kw_args['nickname']
        else:
            nickname = False
         
        if 'email' in all_kw_args:
            email = all_kw_args['email'].lower()
            del all_kw_args['email']  
        else:
            email=False
            
        unique_id = all_kw_args['unique_id'].lower()
        
        all_kw_args['ip_address'] = request.META['REMOTE_ADDR']
        all_kw_args['user_agent'] = request.META['HTTP_USER_AGENT']
        if email:
            try:
                user = User.objects.get(username=email, email=email)
                log.info("#1 User %s requested authentication" % user.username );
            except User.DoesNotExist:
                try:
                    user = User.objects.get(username=unique_id, email="nomail@domain.com")
                    log.info("#1a Updating User %s with email %s" % (user.username, email,) );
                    user.username = email
                    user.email = email
                    user.save()
                except User.DoesNotExist:
                    log.info("#1b Creating User %s" % email );
                    user = User.objects.create_user(email, email=email)    
        else: #anonymous iphone user, no nickname and no email
            try:
                user = User.objects.get(username=unique_id, email="nomail@domain.com")
                log.info("#2 Anonymous User %s logged in" % user.username );
            except User.DoesNotExist:
                user = User.objects.create_user(unique_id, email="nomail@domain.com")
                log.info("#2a Created Anonymous User %s" % user.username );                    

        profile = user.get_profile()
        if nickname:
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
