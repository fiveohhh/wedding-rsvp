from django.template import Context, loader
from rsvp.models import RSVP
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from rsvp.forms import RsvpForm

def index(request):
    return render_to_response('rsvp/index.html', context_instance=RequestContext(request))

def isAttending(request):
    '''
        find out if the user is attending or not
    '''
    try:
        rsvp_id = request.POST['rsvp_id']
        rsvp = RSVP.objects.get(rsvpID=rsvp_id)
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
    form = RsvpForm(instance=rsvp)
    if 'No' in request.POST:
        return render_to_response("rsvp/notAttending.html")
    else:
        return render_to_response("rsvp/getInfo.html", {'rsvp' : rsvp, 'rsvp_form': form}, context_instance=RequestContext(request))

def getInfo(request):
    '''
        Get RSVP info from user
    '''
    rsvp_id = request.session["id"]
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    form = RsvpForm(instance=rsvp)
    if form.is_valid():
        form.save()
        return render_to_response("rsvp/getInfo.html", {'rsvp_form' : form}, context_instance=RequestContext(request))
    else:
        return render_to_response("rsvp/error.html")

def submitInfo(request):
    rsvp_id = request.session["id"]
    rsvp = RSVP.objects.get(rsvpID=rsvp_id)
    
    return HttpResponse(rsvp_id)
