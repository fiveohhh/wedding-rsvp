from django.forms import ModelForm
from rsvp.models import RSVP

class RsvpForm(ModelForm):
    class Meta:
        model = RSVP
        exclude = ('rsvpID', 'allowedAdults', 'allowedChildren', 'rsvpDate')
