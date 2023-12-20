from django.contrib import admin
from mapbox_location_field.admin import MapAdmin
from django import forms
from tinymce.widgets import TinyMCE
from club.models import Club

admin.site.register(Club, MapAdmin)
