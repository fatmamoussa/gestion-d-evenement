from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from datetime import date
from django.views.generic import TemplateView, DeleteView, DetailView, CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from shop.models import Shop
from event.models import Event
from club.models import Club
from connection.models import Activity
from connection.models import Profile
from connection.forms import UserSettingForm, ProfileSettingForm
from django.db.models import Count
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser




from django.shortcuts import render





class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'connection/profile.html'
    #ajouter dans path le nom de l utilisateur connecter 
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
      #Cette ligne récupère l'utilisateur (User) correspondant au nom d'utilisateur spécifié dans le slug de l'URL.
        user = User.objects.get(username=self.kwargs['username'])
        return Profile.objects.get(user=user)
    #recupereation de donnee existant dans la template 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #les derniers shop event club cree
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        #les shops club event cree par l utilisateur 
        context["user_clubs"] = Club.objects.filter(user=self.request.user)
        context["user_shops"] = Shop.objects.filter(user=self.request.user)
        context["user_events"] = Event.objects.filter(user=self.request.user)
        return context


#update profile settings 
# @login_required
# def profileSettings(request, username):
#     template_name = 'connection/settings.html'
#     #recuperation username de l'utilisateur connecter  
#     username = request.user.username
#     if request.method == 'POST':
#         f_user = UserSettingForm(request.POST, instance=request.user)
#         f_profile = ProfileSettingForm(
#             request.POST, request.FILES, instance=request.user.profile)
#         if f_user.is_valid() and f_profile.is_valid():
#             f_user.save()
#             f_profile.save()
#             messages.success(request, _(
#                 "Your information has been successfully updated"))
#             return redirect('profile', username=username)

#     else:
#         f_user = UserSettingForm()
#         f_profile = ProfileSettingForm()

#     if request.method == 'GET':
#         f_user = UserSettingForm(instance=request.user)
#         f_profile = ProfileSettingForm(instance=request.user.profile)

#     context = {
#         'f_user': f_user,
#         'f_profile': f_profile,
#         "shops": Shop.objects.all()[:1],
#         "clubs": Club.objects.all()[:1],
#         "events": Event.objects.all()[:1],
#     }
#     return render(request, template_name, context)
@login_required
def profileSettings(request, username):
    template_name = 'connection/settings.html'
    user = request.user  # Utilisateur connecté
    
    if request.method == 'POST':
        f_user = UserSettingForm(request.POST, instance=user)
        f_profile = ProfileSettingForm(
            request.POST, request.FILES, instance=user.profile)
        if f_user.is_valid() and f_profile.is_valid():
            f_user.save()
            f_profile.save()
            messages.success(request, _("Your information has been successfully updated"))
            return redirect('profile', username=username)

    else:
        f_user = UserSettingForm(instance=user)
        f_profile = ProfileSettingForm(instance=user.profile)

    context = {
        'f_user': f_user,
        'f_profile': f_profile,
        "shops": Shop.objects.all()[:1],
        "clubs": Club.objects.all()[:1],
        "events": Event.objects.all()[:1],
    }
    return render(request, template_name, context)

