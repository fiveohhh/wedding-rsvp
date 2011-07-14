import os, sys
sys.path.append('/home/andy/djangoProjects/weddingRsvp')
sys.path.append('/home/andy/djangoProjects')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
