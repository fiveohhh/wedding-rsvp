from django.template import Context, loader
from rsvp.models import RSVP
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from rsvp.forms import RsvpForm
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
import sys
import datetime

def index(request):
    request.session.flush()
    return render_to_response('rsvp/index.html', context_instance=RequestContext(request))

def isAttending(request):
    '''
        find out if the user is attending or not
    '''
    try:
        rsvp_id = request.POST['rsvp_id']
        rsvp_id = rsvp_id.replace('-','')
        rsvp_id = rsvp_id.upper()
        rsvp = RSVP.objects.get(rsvpID=rsvp_id)
        # check of rsvpDate is null. if it's not, the rsvp has been completed
        if rsvp.rsvpDate:
            errMsg = 'You have already completed your rsvp'
            return render_to_response("rsvp/error.html", {'errorMessage' : errMsg })
        request.session['id'] = rsvp_id
        request.session.set_expiry(300)
        return render_to_response("rsvp/isAttending.html", {'rsvp' : rsvp}, context_instance=RequestContext(request))
    except RSVP.DoesNotExist:
        errMsg = "Unable to find your key, please ensure that it is typed correctly"
        return render_to_response("rsvp/error.html", {'errorMessage' : errMsg})
    except:
        errMsg =  sys.exc_info()[0]
        return render_to_response("rsvp/error.html", {'errorMessage' : errMsg})

def choice(request):
    '''
        View to direct to either get more info if user is coming else mark as not attending.
    '''
    if 'id' not in request.session:
       return HttpResponseRedirect(reverse('rsvp.views.index'))
 
    try:
        rsvp_id = request.session["id"]
        rsvp = RSVP.objects.get(rsvpID=rsvp_id)
        form = RsvpForm(instance=rsvp, max_adults=rsvp.allowedAdults, max_children=rsvp.allowedChildren)
        if 'No' in request.POST:
            request.session['status'] = 2
            rsvp.status = 2
            rsvp.rsvpDate = datetime.datetime.now()
            rsvp.save()
            request.session.flush()
            #send email confirmation
            status = "NOT Attending"

            subject ="RSVP confirmation: " + rsvp.firstName + " " + rsvp.lastName + " is " + status
            body =  "NOT ATTENDING"
            email = EmailMessage(subject, body, to=['andy@chiefmarley.com'])
            email.send()

            return render_to_response("rsvp/notAttending.html")
        else:
            request.session['status'] = 1
            return render_to_response("rsvp/getInfo.html", {'rsvp' : rsvp, 'rsvp_form': form}, context_instance=RequestContext(request))
    except:
        errMsg = sys.exc_info()[0]
        return render_to_response("rsvp/error.html", {'errorMessage' : errMsg})

def getNames(request):
    if 'id' not in request.session:
        return HttpResponseRedirect(reverse('rsvp.views.index'))
    elif not request.POST['email']:
        return HttpResponseRedirect(reverse('rsvp.views.index'))
    rsvp_id = request.session["id"]
    adultsAttending = int(request.POST['adults_attending'])
    childrenAttending = int(request.POST['children_attending'])
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    request.session['adultsAttending'] = adultsAttending
    request.session['childrenAttending'] = childrenAttending
    return render_to_response("rsvp/getNames.html", {'childrenAttending': childrenAttending, 'adultsAttendingRange' : range(adultsAttending), 'childrenAttendingRange' : range(childrenAttending)})

def submitInfo(request):
    if 'id' not in request.session:
       return HttpResponseRedirect(reverse('rsvp.views.index'))
    
    rsvp_id = request.session["id"]
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    adultNames = request.POST.getlist('adultNames')
    kidNames = request.POST.getlist('childrenNames')
    
    # set rsvpStatus
    rsvp.status = request.session['status']
    
    # store names in specialNotes
    strAdults = ' Adults:'
    for s in adultNames:
        strAdults += s + ", "
    strKids = '    Kids:'
    for s in kidNames:
        strKids += s + ", "
    names = strAdults + strKids
    rsvp.specialNotes = names

    rsvp.adultsAttending = request.session['adultsAttending']
    rsvp.childrenAttending = request.session['childrenAttending']

    rsvp.rsvpDate = datetime.datetime.now()

    rsvp.save()

    request.session.flush()
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

