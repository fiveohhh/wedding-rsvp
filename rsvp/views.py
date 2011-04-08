from django.template import Context, loader
from rsvp.models import RSVP
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf


def index(request):
    return render_to_response('rsvp/index.html', context_instance=RequestContext(request))

def isAttending(request):
    try:
        rsvp_id = request.POST['rsvp_id']
        rsvp = RSVP.objects.get(rsvpID=rsvp_id)
        return render_to_response("rsvp/isAttending.html", {'rsvp' : rsvp}, context_instance=RequestContext(request))
    except:
        return render_to_response("rsvp/error.html")

def choice(request):
    rsvp_id = request.POST["rsvpID"]
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    if 'No' in request.POST:
        return render_to_response("rsvp/notAttending.html")
    else:
        return render_to_response("rsvp/getInfo.html", {'rsvp' : rsvp}, context_instance=RequestContext(request))

def getInfo(request):
    rsvp_id = request.POST['rsvpID']
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    form = RSVPForm(instance=rsvp)
    form.save()
    return render_to_response("rsvp/getInfo.html", {'rsvp_form' : form}, context_instance=RequestContext(request))

    
'''
     try:
        rsvp_id = request.POST['rsvpID']
        rsvp = RSVP.objects.get(rsvpID=rsvp_id)
        return render_to_response("rsvp/getInfo.html", {'rsvp' : rsvp,'allowedAdults' : range(rsvp.allowedAdults+1),'allowedChildren' : range(rsvp.allowedChildren+1)}, context_instance=RequestContext(request))
    except:
        return render_to_response("rsvp/error.html")
'''


def submitInfo(request):
    rsvpInfo = request.POST['RSVP']
    rsvp = RSVP.ojects.get(rsvpID=rsvpInfo.rsvpID)
    
