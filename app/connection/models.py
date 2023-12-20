from django.db import models
from datetime import date
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from notifications.models import notify_handler
from notifications.signals import notify
from notifications.models import Notification
from autoslug import AutoSlugField


class NotificationCTA(models.Model):
    #Cela signifie qu'une instance de NotificationCTA est liée à une seule instance de Notification
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    # def custom_notify_handler(*args, **kwargs):
    cta_link = models.CharField(max_length=200, blank=True) 

    def __str__(self):
        return str(self.cta_link)


def custom_notify_handler(*args, **kwargs):
    #Cette ligne appelle le gestionnaire par défaut notify_handler pour obtenir les notifications.
    notifications = notify_handler(*args, **kwargs)
    cta_link = kwargs.get("cta_link", "")
    for notification in notifications:
        NotificationCTA.objects.create(
            notification=notification, cta_link=cta_link)
    return notifications


notify.disconnect(
    notify_handler, dispatch_uid='notifications.models.notification')
# , dispatch_uid='notifications.models.notification')
notify.connect(custom_notify_handler)


class Activity(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='activity/%Y/%M/', default='default.png')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', unique=True)
    activity = models.ManyToManyField(Activity)

    class SubscriberChoises(models.TextChoices):
        PARTICIPANT = '1', _("Participant")
        ORGANIZER = '2', _("Organizer")

    subscriber = models.CharField(
        _("Subscribe as:"), choices=SubscriberChoises.choices, default=SubscriberChoises.PARTICIPANT, max_length=5)
    birthday = models.DateField(_("Birthday"))
    thumbnail = models.ImageField(
        _("Profile image"), upload_to="users/%Y/%M/", default="avatar.png")
    accepted_terms = models.BooleanField(
        _("Terms and condition"), default=False)
 

    def __str__(self):
        #renvoie le nom de user connecter 
        return self.user.username
    #a partir de birthday on calcul l'age
    def age(self):
        if self.birthday:
            today = date.today()
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        else:
            return None#si l utilisateur ne saisi pas son age none est afficher

# @receiver pour connecter la fonction create_or_update_user_profile au signal
#  post_save émis par le modèle User. Cela signifie que lorsque le modèle User est sauvegardé,
#  cette fonction sera appelée.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
