from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^', include('rsvp.urls')),
    (r'^rsvp/', include('rsvp.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^batchimport/', include('batchimport.urls')),
)
   
