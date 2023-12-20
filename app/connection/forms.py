from django import forms
from django.db import models
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, ChangePasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from connection.models import Profile, Activity
from datetime import date
from django.core.exceptions import ValidationError

import re


#formulaire d'inscription signup
class CustomSignupForm(SignupForm):
 

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        if not birthday:
            raise forms.ValidationError(_("Birthday is required."))

        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        if age < 16:
            raise forms.ValidationError(_("You must be at least 16 years old to register."))
        if age > 100:
            raise forms.ValidationError(_("Please provide a valid birthday."))

        return birthday

    
#select des activiter dans formulaire signup 
    activity = forms.ModelChoiceField(
        queryset=Activity.objects.all(),
        required=True,#c est un champs obligatoire 
        empty_label=_("Select an activity")
    )
    accepted_terms = forms.BooleanField(required=True)
    birthday = forms.DateField(required=True)
#l'utilisateur peut etre un organizateur ou un participant
    class SubscriberChoises(models.TextChoices):
        PARTICIPANT = '1', _("Participant")
        ORGANIZER = '2', _("Organizer")
    subscriber = forms.ChoiceField(
        choices=SubscriberChoises.choices, required=True, widget=forms.RadioSelect)

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': _(
            'username'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['email'].widget.attrs.update({'placeholder': _(
            'email'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['password1'].widget.attrs.update({'placeholder': _(
            'password'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['password2'].widget.attrs.update({'placeholder': _(
            'password again'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['activity'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['first_name'].widget.attrs.update({'placeholder': _(
            "First name"), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['last_name'].widget.attrs.update({'placeholder': _(
            "Last name"), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})

    def save(self, request):
        #enregistrer l'utilisateur. 
        user = super(CustomSignupForm, self).save(request)
        user.profile.accepted_terms = self.cleaned_data['accepted_terms']
        user.profile.subscriber = self.cleaned_data['subscriber']
        user.profile.birthday = self.cleaned_data['birthday']
        
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        #Cette ligne ajoute l'activité sélectionnée dans le champ activity du formulaire 
        # à la relation many-to-many activity du profil utilisateur .
        user.profile.activity.add(self.cleaned_data.get('activity'))
        user.save()
        return user
    # def clean_birthday(self):
    #     birthday = self.cleaned_data.get('birthday')

#formulaire s'authentifier login
class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['password'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': _(
            'email'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})


class CustomPasswordChangeForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        user = super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs.update({'placeholder': _(
            'Old password'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-4'})
        self.fields['password1'].widget.attrs.update({'placeholder': _(
            'New password'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-4'})
        self.fields['password2'].widget.attrs.update({'placeholder': _(
            'New password confirmation'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-4'})

        return user


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': _(
            'Old password'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-4'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': _(
            'New password'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-4'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': _(
            'New password confirmation'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-4'})


class UserSettingForm(UserChangeForm):
    password = None
    first_name = forms.CharField(required=True, max_length=10)
    last_name = forms.CharField(required=True, max_length=10)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserSettingForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': _(
            'First name'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500' })
        self.fields['last_name'].widget.attrs.update({'placeholder': _(
            'Last name'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['email'].widget.attrs.update({'placeholder': _(
            'Email'), 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        # Vérifier si le prénom contient des chiffres
        if any(char.isdigit() for char in first_name):
            raise ValidationError(_("Le prénom ne peut pas contenir de chiffres."))
        # Vérifier si le prénom contient des caractères spéciaux
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', first_name):
            raise ValidationError(_("Le prénom ne peut pas contenir de caractères spéciaux."))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        # Vérifier si le nom contient des chiffres
        if any(char.isdigit() for char in last_name):
            raise ValidationError(_("Le nom ne peut pas contenir de chiffres."))
        # Vérifier si le nom contient des caractères spéciaux
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', last_name):
            raise ValidationError(_("Le nom ne peut pas contenir de caractères spéciaux."))
        return last_name

class ProfileSettingForm(forms.ModelForm):
    birthday = forms.DateField(required=True)
    
    class Meta:
        model = Profile
        fields = ['birthday', 'thumbnail']
        
    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        if not birthday:
            raise forms.ValidationError(_("Birthday is required."))

        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        if age < 16:
          raise forms.ValidationError(_("You must be at least 16 years old to register."))
        if age > 100:
            raise forms.ValidationError(_("Please provide a valid birthday."))

        return birthday
    def __init__(self, *args, **kwargs):
        super(ProfileSettingForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['thumbnail'].widget.attrs.update({'class': 'block w-full mb-5 text-xs text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'})
