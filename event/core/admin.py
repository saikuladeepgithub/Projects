# admin.py

from django.contrib import admin
from .models import Faculty
from django.contrib import admin
from .models import Volunteer,galleryimages # Import the Volunteer model


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name', 'email')

admin.site.register(Faculty, FacultyAdmin)
from .models import Event, Review
admin.site.register(Review)

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_approved']
    list_filter = ['is_approved']
    actions = ['approve_events']

    def approve_events(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected events have been approved.")
    approve_events.short_description = "Approve selected events"

admin.site.register(Event, EventAdmin)
from django.contrib import admin
from .models import ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'message', 'timestamp')
    search_fields = ('user__username', 'message', 'event__name')
    list_filter = ('event', 'timestamp')

admin.site.register(ChatMessage, ChatMessageAdmin)

from django.contrib import admin
from .models import Volunteer

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'activities', 'phone_number')
    search_fields = ('user__username', 'event__name', 'activities', 'phone_number')
    list_filter = ('event', 'activities')

@admin.register(galleryimages)
class galleryadmin(admin.ModelAdmin):
    list_display=('event','user','caption')