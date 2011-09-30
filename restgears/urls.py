from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf.urls.static import static
from django.conf import settings
from base.views import Overview

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'restgears.views.home', name='home'),
                       (r'^$', Overview.as_view()),
                       (r'^news/', include('publisher.urls')),
                       (r'^gallery/', include('gallery.urls')),
                       (r'^account/', include('account.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin:
                       (r'^admin/', include(admin.site.urls)),
                       (r'^', include('base.urls')),
                       (r'^', include('djangorestframework.urls')),
                       
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
