A ChiPy AntiSpam Demo
=====================
* Author: Paul Ebreo
* Experience level: newbie
* Interests: Python, Django, and Javascript

Purpose
=======
A common problem with maintaining a website is filtering out spam.
This Django project demonstrates how to implement a "honeypot" approach to
filter spam from the ChiPy RSVP submission form. 

Basic Algorithm
===============
A honeypot is any enticing trap meant to alert a person trying to fight unwanted behavior. 
In this case, the unwanted behavior is spambots automatically filling out the the ChiPy RSVP form. 
The honeypot will be hidden HTML fields which our Django view will perform logic on.

To implement the honey pot, I added two extra form fields to the RSVP popup 
dialog and hid them using jQuery. Those two fields are the "address" field and "phone" field.
   
    <div id="supplementary-fields" style="diplay:block"> 
        <label id="phone" for="phone">Phone</label>
        <input id="phone_field" type="text" name="phone" placeholder="708-588-2300">                       
        <label id="address" for="address">Address</label>
        <input id="address_field" type="text" name="address" placeholder="323 N Wacker">
    </div> 


To hide the honeypot fields, this is the jQuery method that's called when the form dialog is open:

    $('#supplementary-fields').css("display", "none");

Spambots will indiscriminately fill out the fields and our Django view will
handle the POST data appropriately by **rejecting any form submits that have 
the hidden "phone" or "address" filled out.** This is what the view will look like to handle
the form POST:

      def rsvp(request):
         """ A view to handle the RSVP form submission """
         if request.method == 'POST':
            try:
               """ Accept if neither ('address' or 'post') are filled in """
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


It is not very sophisticated but it is a decent first iteration of the honeypot algorithm.
There's room for a lot of improvement. :)



Django unit tests
============
For this project I made 7 unit test methods.
* Form submission tests:
  - Test the RSVP form submit view handling valid data
  - Test the RSVP form submit view handling invalid data
  
* RSVP ListView tests:
  - Test the ListView to handle no people on the rsvp list
  - Test the ListView to handle when people are on the list
* Main page tests:
  - Test the index view to handle the home page with valid contexts
  - Test the index view to handle invalid contexts
* Message page test:
  - Test a view that handles "About", "Recent Topics", "Give a Talk", 
"Contact" and "Login" links on home page

For this project, the most important unittests are the form submission
tests which look like this:


      
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

And to test invalid form submissions:


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
        

Installation & Requirements
======================
This project utilizes:
- Django 1.5
- Psycopg2
- PostgreSQL db

To install this project just clone this repo and change the `local_settings.py`
to your local postgresql db settings and login information. The `local_settings.py` overrides the `settings.py` file.

You must have a local PostgreSQL server running. In my case, I installed PostgreSQL with the following setup:

    db name: postgres
    db username: postgres
    pw: 1234
    PORT: 54321

When you're done with the settings just run `python manage.py runserver` and goto `http://localhost:8000/chipy/`. 
