from django.conf.urls.defaults import *

urlpatterns = patterns('rsvp.views',
    (r'^$', 'index'),
    (r'^submitInfo/$', 'submitInfo'),
    (r'^choice/$', 'choice'),
    (r'^isAttending/$', 'isAttending'),
    (r'^getNames/$', 'getNames'),
    (r'^submitInfo/$', 'submitInfo'),

)
   
