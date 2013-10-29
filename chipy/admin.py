from django.contrib import admin
from chipy.models import Meeting
from chipy.models import Venue
from chipy.models import Person

class MeetingAdmin(admin.ModelAdmin):
	class Meta:
		model = Meeting
	
class VenueAdmin(admin.ModelAdmin):
	class Meta:
		model = Venue
	
class PersonAdmin(admin.ModelAdmin):
	class Meta:
		model = Person
	
admin.site.register(Meeting)
admin.site.register(Venue)
admin.site.register(Person)
