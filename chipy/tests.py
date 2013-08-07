"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.core.urlresolvers import reverse
from chipy.models import Meeting, Person
import datetime
from django.utils import timezone


def create_person(name, email, ynm):
    """ Creates a Person """
    return Person.objects.create(name=name,email=email,ynm=ynm)

def create_meeting(topic, when):
    """ Create Meeting """
    return Meeting.objects.create(topic=topic,when=when)



class RsvpFormSubmitTests(TestCase):


    def test_rsvp_form_submit_view_valid(self):
        """ A valid form should have blank phone and address data """
        post_kwargs = {'checkbox':'',
                    'name':'john',
                    'submit':'RSVP',
                    'response':'Y',
                    'phone':'', # there should be blank phone
                    'address':'', # there should be blank address
                    'csrfmiddlewaretoken':'1234',
                    'meeting':'sometime',
                    'email':'john@yahoo',

        }
        create_person('john','john@yahoo.com','Y')
        response = self.client.post(reverse('chipy:rsvp'),post_kwargs)

        self.assertEqual(response.status_code,302) # redirect


        # or, to use assertRedirect() to index view, you have to create Model objects
        #create_person('john','john@yahoo.com','Y')
        #create_meeting('food',timezone.now())
        #redirect = reverse('chipy:index')
        #self.assertRedirects(response, redirect)


    def test_rsvp_form_submit_view_invalid_submission(self):
        """ An invalid submit will have phone and/or address filled in
            Spambots would fill in those hidden fields
        """
        post_kwargs = {'checkbox':'',
                    'name':'john',
                    'submit':'RSVP',
                    'response':'Y',
                    'phone':'773-588-2300',
                    'address':'1 main st',
                    'csrfmiddlewaretoken':'1234',
                    'meeting':'sometime',
                    'email':'john@yahoo',

        }

        response = self.client.post(reverse('chipy:rsvp'),post_kwargs)

        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Not a valid rsvp submission")

class RsvpViewTests(TestCase):


    def test_rvsp_list_view_with_no_persons(self):
        """ The ListView should handle now Person objects and display a message in template """
        response = self.client.get(reverse('chipy:rsvp_list'))
        self.assertEqual(response.status_code,200)

        self.assertContains(response,"No persons are available.") # must be somewhere in rsvp_list.html
        self.assertQuerysetEqual(response.context['rsvplist'],[])


    def test_rsvp_list_with_persons_in_list(self):
        """ The ListView should work with 1 or more Person objects in the db """
        create_person('john','john@yahoo.com','Y')
        response = self.client.get(reverse('chipy:rsvp_list'))
        self.assertEqual(response.status_code,200)

        self.assertQuerysetEqual(response.context['rsvplist'],['<Person: john>'])


class IndexViewTests(TestCase):


    def test_index_view(self):
        """ The DetailView should work when there are Person and Meeting objects  """
        create_person('john','john@yahoo.com','Y')
        create_meeting('food',timezone.now())
        response = self.client.get(reverse('chipy:index'))
        self.assertEqual(response.status_code,200)

    def test_index_view_no_objects(self):
        """ The DetailView should work redirect to 404 when no Person or Meeting objects """
        response = self.client.get(reverse('chipy:index'))
        self.assertEqual(response.status_code,404)


class MessagePageViewTests(TestCase):

    def test_message_page_view(self):
        response = self.client.get(reverse('chipy:message_page',args=['somepage']))
        self.assertEqual(response.status_code,200)

