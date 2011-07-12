from django.conf.urls.defaults import *
from django import forms
from django.forms import ModelForm
from account.views import AccountOverviewView, RetrieveCredentialsView
from account.models import DeviceAuthToken

from djangorestframework.resources import ModelResource

class DeviceAuthTokenForm(ModelForm):
    email = forms.EmailField()
    nickname = forms.CharField()
    class Meta:
        model = DeviceAuthToken
        fields = ('unique_id',)

class DeviceAuthTokenResource(ModelResource):
    model = DeviceAuthToken
    form = DeviceAuthTokenForm
    exclude = ('url',)

urlpatterns = patterns ('',
    url(r'^$', AccountOverviewView.as_view(), name ='account-overview'),
    url(r'^retrieve-credentials$', RetrieveCredentialsView.as_view(resource=DeviceAuthTokenResource), name='account-retrieve-credentials'),
)
