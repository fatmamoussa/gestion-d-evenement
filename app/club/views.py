from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, DetailView, CreateView, ListView, UpdateView
from club.forms import ClubForm
from shop.models import Shop
from event.models import Event
from club.models import Club
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateClubView(CreateView):
    template_name = 'club/index.html'
    model = Club
    form_class = ClubForm
    success_message = _("%(name)s was created successfully")

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        has_club = Club.objects.filter(user=user).exists()

        if has_club:
            messages.error(self.request, "You are already have a club!")
            return redirect('home')  # Remplacez 'home' par le nom de votre vue ou URL de destination

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        return context


class UpdateClubView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Club
    form_class = ClubForm
    template_name = "club/index.html"
    success_message = _("%(name)s was updated successfully")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.request.user
        obj = form.save(commit=False)
        if not obj.user == self.request.user:
            messages.error(
                self.request, "You are not authorized to update this club.")
            return redirect('club', slug=obj.slug)
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        return context


class DeleteClubView(LoginRequiredMixin, DeleteView):
    model = Club
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return Club.objects.get(slug=slug)

    def delete(self, request, *args, **kwargs):
        club = self.get_object()
        if club.event_set.exists():
            messages.error(self.request, _("Cannot delete the club because it has created events"))
            return self.handle_no_permission()
        
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, _("Your club has been deleted"))
        return response





    
class ListClubView(ListView):
    model = Club
    paginate_by = 10
    template_name = "club/list.html"


class ClubView(DetailView):
    model = Club
    template_name = 'club/club.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        return context
