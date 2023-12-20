from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from mapbox_location_field.models import LocationField, AddressAutoHiddenField
from autoslug import AutoSlugField
from django.core.validators import RegexValidator
from django.urls import reverse_lazy, reverse
from phonenumber_field.modelfields import PhoneNumberField
from tinymce import models as tinymce_models
from club.models import Club
from shop.models import Shop
from django.core.exceptions import ValidationError

class Event(models.Model):
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    #user,on_delete=models.CASCADE lorsque l utilisateur est supprimer tout object de l'utilsateur doit etre supprimer 
    #slug est utiliser pour cree des urls lisible par l homme pour amelioer l experience uilisateur 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_("Name of the event"), max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    location = LocationField(_("Location"))
    address = AddressAutoHiddenField(_("Address"))
    description = tinymce_models.HTMLField(_("Description"))
    thumbnail = models.ImageField(
        _("Feature image"), upload_to="events/%Y/%M/", default="default.png")
   
    likes = models.ManyToManyField(
        User, default=None, blank=True, related_name='likes')#r plusieurs utilisateurs aimant plusieurs événements.
    event_date = models.DateField(_("Event date"))
   

    max_subscriber = models.PositiveIntegerField(_("Max number of subscribe"))
    minor = models.BooleanField(_("Minor authorization"), default=False)
    framing_device = models.BooleanField(_("Framing device"), default=False)
    camera_man = models.BooleanField(_("Camera man"), default=False)
    body_protection = models.BooleanField(_("Body protection"), default=False)
    authorization = models.FileField(
        _("authorization"), upload_to="events/authorization/%Y/%M/", blank=True, null=True)#tu peut laisser le champs vide blank=True, null=True

    class LevelChoises(models.TextChoices):
        pro = '1', _("Professional")
        beginner = '2', _("Beginner")
    level = models.CharField(_("Choose the level :"), choices=LevelChoises.choices,
                             default=LevelChoises.beginner, max_length=5, blank=True)
    helmet = models.BooleanField(_("Helmet"), default=False)
    safety_vest = models.BooleanField(_("Safety vest"), default=False)
    bicycle_pump = models.BooleanField(_("Bicycle pump"), default=False)

    class Mototypes(models.TextChoices):
        moto1 = '1', _("The supermotards")
        moto2 = '2', _("Sports")
        moto3 = '3', _("Trails")
        moto4 = '4', _("Roadsters")
        moto5 = '5', _("Road")
        moto6 = '6', _("125 cm3")
        moto7 = '7', _("Basics")
    moto_type = models.CharField(_("Choose a type of motobike:"), choices=Mototypes.choices,
                                 default=Mototypes.moto7, max_length=5, blank=True)

    class Bicycletypes(models.TextChoices):
        bike1 = '1', _("Electric")
        bike2 = '2', _("Fatbike")
        bike3 = '3', _("Mountain")
        bike4 = '4', _("Gravel")
        bike5 = '5', _("Hybrid")
        bike6 = '6', _("Urban")
    bicycle_type = models.CharField(_("Choose a type of bicycle:"), choices=Bicycletypes.choices,
                                    default=Bicycletypes.bike6, max_length=5, blank=True)

    class Hikingtypes(models.TextChoices):
        type1 = '1', _("The Stroll")
        type2 = '2', _("Long hike and trekkin")
        type3 = '3', _("Technical hiking and mountaineering")
    hiking_type = models.CharField(_("Choose a type of hiking:"), choices=Hikingtypes.choices,
                                   default=Hikingtypes.type1, max_length=5, blank=True)
    good_shoes = models.BooleanField(_("Good shoes"), default=False)
    walking_stick = models.BooleanField(_("Walking stick"), default=False)
    tent = models.BooleanField(_("Tent"), default=False)
    transport = models.BooleanField(_("Transport"), default=False)
    anti_slip_shoes = models.BooleanField(_("Anti slip shoes"), default=False)
    snow_stick = models.BooleanField(_("Snow stick"), default=False)
    warm_and_weatherproof_clothing = models.BooleanField(
        _("Warm and weatherproof clothing"), default=False)
    medical_certificate = models.ImageField(
        _("Medical certificate"), upload_to="events/certificate/%Y/%M/", blank=True, null=True)
#django ajoute s pour les table pour que le frnacais soit correct il est preferable d ajoutet la class meta
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
    #l'utilisateur doit choisir entre l evenement appartient club ou shop
    def clean(self):
        if self.club and self.shop:
            raise ValidationError("Vous ne pouvez choisir qu'un seul élément : club ou shop.")

    def save(self, *args, **kwargs):
        self.clean()
        #clean est appelée pour valider l'instance. 
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()
    # utilisé pour identifier l'événement dans l'URL.
    def get_absolute_url(self):
        return reverse("event", kwargs={"slug": self.slug})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField(_('Send a message'))

    class Meta:
        ordering = ['created_on']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return '%s - replied by: %s' % (self.event.slug, self.user)
