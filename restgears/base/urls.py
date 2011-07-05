from django.conf.urls.defaults import *
from base import views

urlpatterns = patterns ('',
                        (r'^image/(?P<pk>\w+)$', views.image_download_handler),
)
