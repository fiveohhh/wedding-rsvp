from django.db import models
from django.forms import ModelForm
import datetime
	
class RSVP (models.Model):
	def __unicode__(self):
		return self.firstName + " " + self.lastName
	STATUS_CHOICES = (("0", "No Response"), ("1", "Attending"), ("2", "NOT attending"))
	status = models.CharField(max_length=1, choices = STATUS_CHOICES, default = "No Response") 
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=30)
	rsvpID = models.CharField(max_length=9, unique = True)
	allowedAdults = models.IntegerField(default = 2)
	allowedChildren = models.IntegerField(default = 0)
	adultsAttending = models.IntegerField(default = 0)
	childrenAttending = models.IntegerField(default = 0)
	rsvpDate = models.DateTimeField('date of rsvp', null = True, blank = True)
	email = models.EmailField(max_length=50)
	specialNotes = models.CharField(max_length=255)
	
class RSVPForm(ModelForm):
	class Meta:
		model = RSVP
		exclude = ('rsvpID', 'allowedAdults', 'allowedChildren', 'rsvpDate')	
