from django.contrib import admin

# Register your models here.
from .models import UserProfile, TravelPlan, Destination, Attraction, Itinerary, TravelItem, TravelPreference

admin.site.register(UserProfile)
admin.site.register(TravelPlan)
admin.site.register(Destination)
admin.site.register(Attraction)
admin.site.register(Itinerary)
admin.site.register(TravelItem)
admin.site.register(TravelPreference)
