from django.contrib import admin
from shop.models import Shop
from mapbox_location_field.admin import MapAdmin  

admin.site.register(Shop, MapAdmin)