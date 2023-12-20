from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from mapbox_location_field.models import LocationField, AddressAutoHiddenField
from autoslug import AutoSlugField
from django.core.validators import RegexValidator
from django.urls import reverse_lazy, reverse
from phonenumber_field.modelfields import PhoneNumberField
from tinymce import models as tinymce_models

class Shop(models.Model):
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_("Name of the store"), max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    location = LocationField(_("Location"))
    address = AddressAutoHiddenField(_("Address"))
    description = tinymce_models.HTMLField(_("Description"))
    thumbnail = models.ImageField(_("Logo"), upload_to="shops/%Y/%M/", default="default.png")
    phone = PhoneNumberField(_("Phone"), blank=True)
    email = models.EmailField(_("Email"), max_length=255)
    site = models.URLField(_("Website"), max_length=255, blank=True, null=True)
    instagram = models.URLField(_("Instagram"), max_length=255, blank=True, null=True)
    facebook = models.URLField(_("Facebook"), max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop", kwargs={"slug": self.slug})