from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, DetailView, CreateView, ListView, UpdateView
from shop.forms import ShopForm
from shop.models import Shop
from event.models import Event
from club.models import Club
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateShopView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Shop
    form_class = ShopForm
    template_name = "shop/index.html"
    success_message = _("%(name)s was created successfully")

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        return context


class UpdateShopView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Shop
    form_class = ShopForm
    template_name = "shop/index.html"
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
                self.request, "You are not authorized to update this shop.")
            return redirect('shop', slug=obj.slug)
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        return context


class DeleteShopView(LoginRequiredMixin, DeleteView):
    model = Shop
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return Shop.objects.get(slug=slug)

    def delete(self, request, *args, **kwargs):
        shop = self.get_object()
        if shop.event_set.exists():
            messages.error(self.request, _("Cannot delete the shop because it has created events"))
            return self.handle_no_permission()
        
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, _("Your shop has been deleted"))
        return response


class ListShopView(ListView):
    model = Shop
    template_name = "shop/list.html"
    paginate_by = 10


class ShopView(DetailView):
    model = Shop
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        return context
