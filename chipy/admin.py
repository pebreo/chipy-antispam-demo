from django.contrib import admin
from chipy.models import Meeting
from chipy.models import Venue
from chipy.models import Person


admin.site.register(Meeting)

admin.site.register(Venue)

admin.site.register(Person)