from django.db import models
from django.utils.translation import gettext as _
from autoslug import AutoSlugField
from django.urls import reverse_lazy, reverse
from tinymce import models as tinymce_models
from club.models import Club
from event.models import Event

class Page(models.Model):
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    title = models.CharField(_("Page title"), max_length=250)
    slug = AutoSlugField(populate_from='title')
    text_en = tinymce_models.HTMLField(_("Text English"))
    text_fr = tinymce_models.HTMLField(_("Text Frensh"))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("page", kwargs={"slug": self.slug})


class Contact(models.Model):
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    email = models.EmailField(_("Email"), max_length=254)
    first_name = models.CharField(_("First name"), max_length=250)
    last_name = models.CharField(_("Last name"), max_length=250)
    subject = models.CharField(_("Subject"), max_length=250)
    message = models.TextField(_("Message"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("contact", kwargs={"pk": self.pk})

