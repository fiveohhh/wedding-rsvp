from django.template import Context, loader
from rsvp.models import RSVP
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from rsvp.forms import RsvpForm
from django.core.mail import EmailMessage

import datetime

def index(request):
    return render_to_response('rsvp/index.html', context_instance=RequestContext(request))

def isAttending(request):
    '''
        find out if the user is attending or not
    '''
    try:
        rsvp_id = request.POST['rsvp_id']
        rsvp = RSVP.objects.get(rsvpID=rsvp_id)
        if str(rsvp.status) != '0':
            errMsg = "It appears that you have already submitted your RSVP on " + str(rsvp.rsvpDate) + "\r\n" + 
                       "Please contact us at 952.843.3290 if this is not the case"
            return render_to_response("rsvp/error.html", {'errorMessage' :errMsg} )
	request.session['id'] = rsvp_id
        return render_to_response("rsvp/isAttending.html", {'rsvp' : rsvp}, context_instance=RequestContext(request))
    except:
        return render_to_response("rsvp/error.html")

def choice(request):
    '''
        View to direct to either get more info if user is coming else mark as not attending.
    '''
    rsvp_id = request.session["id"]
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    form = RsvpForm(instance=rsvp, max_adults=rsvp.allowedAdults, max_children=rsvp.allowedChildren)
    if 'No' in request.POST:
        request.session['status'] = 2
        return render_to_response("rsvp/notAttending.html")
    else:
        request.session['status'] = 1
        return render_to_response("rsvp/getInfo.html", {'rsvp' : rsvp, 'rsvp_form': form}, context_instance=RequestContext(request))

def getNames(request):
    rsvp_id = request.session["id"]
    adultsAttending = int(request.POST['adults_attending'])
    childrenAttending = int(request.POST['children_attending'])
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    request.session['adultsAttending'] = adultsAttending
    request.session['childrenAttending'] = childrenAttending
    return render_to_response("rsvp/getNames.html", {'childrenAttending': childrenAttending, 'adultsAttendingRange' : range(adultsAttending), 'childrenAttendingRange' : range(childrenAttending)})

def submitInfo(request):
    rsvp_id = request.session["id"]
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    adultNames = request.POST.getlist('adultNames')
    kidNames = request.POST.getlist('childrenNames')
    
    # set rsvpStatus
    rsvp.status = request.session['status']
    
    # store names in specialNotes
    strAdults = 'Adults:'
    for s in adultNames:
        strAdults += s + ", "
    strKids = 'Kids:'
    for s in kidNames:
        strKids += s + ", "
    names = strAdults + strKids
    rsvp.specialNotes += names

    rsvp.adultsAttending = request.session['adultsAttending']
    rsvp.childrenAttending = request.session['childrenAttending']

    rsvp.rsvpDate = datetime.datetime.now()

    rsvp.save()

    request.session['rsvpCompleteed'] = 1
    
    #send email confirmation
    status = ""
    if rsvp.status == 1:
        status = "Attending"
    elif rsvp.status == 2:
        status = "NOT Attending"

    subject ="RSVP confirmation: " + rsvp.firstName + " " + rsvp.lastName + " is " + status
    body =  "Attendees:" + rsvp.specialNotes
    email = EmailMessage(subject, body, to=['andy@chiefmarley.com'])
    email.send()

    return render_to_response("rsvp/thankYou.html", {'email':rsvp.email})

