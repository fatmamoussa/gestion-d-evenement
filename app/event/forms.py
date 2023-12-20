from django import forms
from event.models import Event, Comment
from django.utils.translation import gettext_lazy as _
from datetime import date
from .models import Club, Shop
from django.urls import reverse
import re

from datetime import date, timedelta



class EventForm(forms.ModelForm):
    club_or_shop = forms.ChoiceField(choices=(), required=True)
  




    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < date.today():
            raise forms.ValidationError(
                _("The date of the event cannot be earlier than today's date."))
        
        if event_date:
            today = date.today()
            max_date = today + timedelta(days=365 * 6)  # Ajout de 6 ans à la date actuelle
            if (event_date - today).days > (365 * 6):
                raise forms.ValidationError(
                    _("La date de l'événement ne peut pas être supérieure à 6 ans à partir de la date actuelle."))
        
        return event_date
    def clean_max_subscriber(self):
        max_subscriber=self.cleaned_data.get('max_subscriber')
        if max_subscriber == 0:
            raise forms.ValidationError(
                    _("le number maximum doit etre 1 minimum"))
        
        return max_subscriber
 
        
        


    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9\sÀ-ÿ]+$', name):
            raise forms.ValidationError("Le nom ne doit contenir que des lettres, des chiffres et des accents.")
        return name

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        clubs = Club.objects.filter(user=user)
        shops = Shop.objects.filter(user=user)
# Cette ligne construit une liste contient nom de club et shop .
        choices = [("", "Select a shop or club")] + [(f"club_{club.pk}", club.name)
                                                     for club in clubs] + [(f"shop_{shop.pk}", shop.name) for shop in shops]

        self.fields['club_or_shop'].choices = choices
        self.fields['club_or_shop'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
        })

        self.fields['name'].widget.attrs.update(
            {'placeholder': _('Name'), 'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['max_subscriber'].widget.attrs.update(
            {'placeholder': 'Max subscriber', 'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['description'].widget.attrs.update(
            {'placeholder': _('Description'), 'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-200 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['event_date'].widget.attrs.update(
            {'placeholder': _('Description'), 'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-200 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['thumbnail'].widget.attrs.update(
            {'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'})
        self.fields['minor'].widget.attrs.update({'class': 'sr-only peer'})
        self.fields['framing_device'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['camera_man'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['body_protection'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['helmet'].widget.attrs.update({'class': 'sr-only peer'})
        self.fields['safety_vest'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['bicycle_pump'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['good_shoes'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['walking_stick'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['tent'].widget.attrs.update({'class': 'sr-only peer'})
        self.fields['transport'].widget.attrs.update({'class': 'sr-only peer'})
        self.fields['anti_slip_shoes'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['snow_stick'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['warm_and_weatherproof_clothing'].widget.attrs.update(
            {'class': 'sr-only peer'})
        self.fields['level'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['moto_type'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['bicycle_type'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['hiking_type'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['medical_certificate'].widget.attrs.update(
            {'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'})
        self.fields['authorization'].widget.attrs.update(
            {'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'})

    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['user', 'club', 'shop']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update(
            {'class': 'block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'rows': 1})

    def get_action_url(self):
        return reverse('update_comment', kwargs={'slug': self.slug, 'pk': self.pk})


class CommentDeleteForm(forms.Form):
    confirm_delete = forms.BooleanField(required=True)



    