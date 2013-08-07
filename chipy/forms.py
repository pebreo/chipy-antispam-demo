from django import forms
from django.db import models

class RsvpForm(forms.Form):
    """ I didn't get a chance to use this """
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
