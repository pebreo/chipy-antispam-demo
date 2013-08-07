# Create your views here.
#http
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render
# generic
from django.views import generic # generic views
# models
from chipy.models import Meeting
from chipy.models import Person
#misc
from django.utils import timezone


def rsvp(request):
    """ A view to handle the RSVP form submission """
    if request.method == 'POST':
        try:
            """ Create if neither ('address' or 'post') are filled in """
            if not (request.POST['address'] or request.POST['phone']):
                person = Person(name=request.POST['name'],
                                email=request.POST['email'],
                                ynm=request.POST['response'])
                person.save()

                return HttpResponseRedirect(reverse('chipy:index'))
            else:

                return HttpResponse("Not a valid rsvp submission")
        except Person.DoesNotExist:
            raise Http404


    return HttpResponseRedirect(reverse('chipy:index'))



class RsvpListView(generic.ListView):
    """ A view show the list of people that said 'Yes' to the RSVP form """
    template_name = 'chipy/rsvp_list.html'
    context_object_name = 'rsvplist'

    def get_queryset(self):
        return Person.objects.filter(ynm='Y')


def index(request):
    """ Home page view for chipy """
    try:
        meeting = Meeting.objects.latest('when')
        num_rsvped = Person.objects.filter(ynm='Y').count()

    except (KeyError, Meeting.DoesNotExist, Person.DoesNotExist):
        raise Http404

    return render(request,'chipy/chipy.html',{'meeting':meeting,'num_rsvped':num_rsvped})


def message_page(request,page_name):
    """ Redirect 'About', 'Recent Topics', 'Give a Talk', etc  """
    return HttpResponse("This will be the {0} page.".format(page_name))





