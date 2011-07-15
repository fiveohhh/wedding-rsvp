from rsvp.models import RSVP
from django.contrib import admin
from rsvp.actions import export_as_csv


class MyAdmin(admin.ModelAdmin):
	actions = [export_as_csv]

admin.site.register(RSVP, MyAdmin)
