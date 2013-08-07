from django.db import models
from django.forms import ModelForm
from django.utils import timezone
import datetime


class Meeting(models.Model):
    topic = models.CharField(max_length=200)
    when = models.DateTimeField('meeting date')

    def __unicode__(self):
        return self.topic

class Venue(models.Model):
    meeting = models.ForeignKey(Meeting)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=400)

    def __unicode__(self):
        return self.name

class Person(models.Model):

    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    ynm = models.CharField(max_length=10) # yes, no, maybe

    def __unicode__(self):
        return self.name
