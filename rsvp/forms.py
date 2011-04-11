from django.forms import ModelForm
from rsvp.models import RSVP
from django import forms

class RsvpForm(ModelForm):
    class Meta:
        model = RSVP
        exclude= ('firstName', 'lastName','adultsAttending' ,'childrenAttending','status' ,'rsvpID', 'allowedAdults', 'allowedChildren', 'rsvpDate')
    def __init__(self, *args, **kwargs):
        max_adults = kwargs.pop('max_adults', 2)
        max_children = kwargs.pop('max_children',0)

        super(RsvpForm, self).__init__(*args, **kwargs)

        adult_choices = ( (x,str(x)) for x in range(max_adults+1)) 
        children_choices = ( (x,str(x)) for x in range(max_children+1)) 

        self.fields['adults_attending'] = forms.ChoiceField(choices = adult_choices)
        self.fields['children_attending'] = forms.ChoiceField(choices = children_choices)
