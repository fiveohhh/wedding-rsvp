from django.conf.urls.defaults import *

urlpatterns = patterns('rsvp.views',
    (r'^$', 'index'),
    (r'^getInfo/$', 'getInfo'),
    (r'^choice/$', 'choice'),
    (r'^isAttending/$', 'isAttending'),
    (r'^submitInfo/$', 'submitInfo'),
)
   
