from django.contrib import admin
from mapbox_location_field.admin import MapAdmin
from event.models import Event, Comment

#la creation de table event et comment dans la base de donnee
admin.site.register(Event, MapAdmin)
admin.site.register(Comment)
