from django.core.urlresolvers import reverse

from djangorestframework.views import View, ModelView
from djangorestframework.mixins import InstanceMixin, ReadModelMixin, DeleteModelMixin, UpdateModelMixin, CreateModelMixin, AuthMixin



class AccountOverviewView(View):
    """Welcome to the Account Module.

    """
    def get(self, request):
        return [{'name': 'Account Retrieve Credentials', 'url': reverse('account-retrieve-credentials')},]

class RetrieveCredentialsView(View):
    def post(self, request, *args, **kwargs):
        #kwargs.update({'user_id':kwargs['user_id'],
        #               'gallery_id':kwargs['pk'],
        #               })
        #del kwargs['pk']
        #all_kw_args = dict(self.CONTENT.items() + kwargs.items())
        #logger = logging.getLogger(__name__)
        #logger.info("Returning from BlobStore, kwargs: %s, "%(all_kw_args))
        #super(PostPhotoUploadView, self).post(request, *args, **kwargs)
        return {'username':'andre',
                'password':'tester',
                'created':False,},
