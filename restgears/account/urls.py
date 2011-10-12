from django.conf.urls.defaults import *
from django import forms
from account.views import AccountOverviewView, RetrieveCredentialsView
from account.models import DeviceAuthToken

from djangorestframework.resources import ModelResource

class DeviceAuthTokenForm(forms.Form):
    email = forms.EmailField(required=False)
    nickname = forms.CharField(required=False)
    unique_id = forms.CharField()

class DeviceAuthTokenResource(ModelResource):
    model = DeviceAuthToken
    form = DeviceAuthTokenForm
    exclude = ('url',)

urlpatterns = patterns ('',
    url(r'^$', AccountOverviewView.as_view(), name ='account-overview'),
    url(r'^retrieve-credentials$', RetrieveCredentialsView.as_view(resource=DeviceAuthTokenResource), name='account-retrieve-credentials'),
)
