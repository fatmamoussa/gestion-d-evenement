import json
from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, DetailView, CreateView 


from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.contrib.auth.models import User
from event.models import Event
from club.models import Club
from shop.models import Shop
from public.models import Page, Contact 
from public.forms import ContactForm
from django.db.models import Count
from connection.models import Activity
from connection.models import Profile






class HomeView(TemplateView):
    template_name = 'public/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Event
        events = Event.objects.all()
        event_data = [{
            'location': event.location,
            'name': event.name,
            'date': event.event_date.strftime('%d/%m/%Y'),
            'address': event.address,
            'url': event.get_absolute_url(),
        } for event in events]
        # Shops
        shops = Shop.objects.all()
        shop_data = [{
            'location': shop.location,
            'name': shop.name,
            'thumbnail': shop.thumbnail.url,
            'address': shop.address,
            'url': shop.get_absolute_url(),
        } for shop in shops]
        # Clubs
        clubs = Club.objects.all()
        club_data = [{
            'location': club.location,
            'name': club.name,
            'thumbnail': club.thumbnail.url,
            'address': club.address,
            'url': club.get_absolute_url(),
        } for club in clubs]
        event_data_json = json.dumps(event_data)
        shop_data_json = json.dumps(shop_data)
        club_data_json = json.dumps(club_data)
        context["event_data"] = event_data_json
        context["shop_data"] = shop_data_json
        context["club_data"] = club_data_json
        return context

class AboutView(TemplateView):
     template_name = 'public/about.html'

class MyChartView(TemplateView):
    template_name = 'public/chart.html'


    # 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # activity 
        acts = []
        context["user_activity"] = Profile.objects.values('activity').annotate(count=Count('activity'))
        # print(context["user_activity"])
        for act in context["user_activity"]:
            acts_filter = Activity.objects.filter(id=act['activity'])
            #print(acts_filter)
            if acts_filter.exists():
                acts.append(acts_filter[0].name)  # Ajoute le nom de l'activité à la liste 'acts'

        context['acts'] = acts
        #print("cccc", context['acts'])
        nbr_act = [act['count'] for act in context["user_activity"]]  # Liste des valeurs de 'count'
        # print("nbr_act", nbr_act)
        context['nbr_act'] = nbr_act
        # subscriber
        events = Event.objects.annotate(subscriber_count=Count('likes'))
        
        event_names = [event.name for event in events]
        subscriber_counts = [event.subscriber_count for event in events]
        
        context['event_names'] = event_names
        context['subscriber_counts'] = subscriber_counts
        # Obtenir les noms des clubs et le nombre d'événements créés par club
        club_events = (
            Club.objects.annotate(num_events=Count('event'))
            .values('name', 'num_events')
        )
        # nb des events par club
        # Créer les listes pour les labels et les données du graphique
        labels = []
        data = []

        # Parcourir les résultats et ajouter les noms des clubs et le nombre d'événements aux listes
        for club_event in club_events:
            labels.append(club_event['name'])
            data.append(club_event['num_events'])

        # Ajouter les listes au contexte
        context['labels'] = labels
        context['data'] = data
        shop_events = (
            Shop.objects.annotate(num_events=Count('event'))
            .values('name', 'num_events')
        )

        # Créer les listes pour les labels et les données du graphique pour les shops
        shop_labels = []
        shop_data = []

        # Parcourir les résultats et ajouter les noms des shops et le nombre d'événements aux listes
        for shop_event in shop_events:
            shop_labels.append(shop_event['name'])
            shop_data.append(shop_event['num_events'])

        # Ajouter les listes au contexte
        context['shop_labels'] = shop_labels
        context['shop_data'] = shop_data
        # Calculer le nombre total d'événements pour les clubs et les shops
        total_club_events = sum(data)
        total_shop_events = sum(shop_data)

        # Calculer les pourcentages totaux des événements pour les clubs et les shops
        club_percentage_total = (total_club_events / (total_club_events + total_shop_events)) * 100
        shop_percentage_total = (total_shop_events / (total_club_events + total_shop_events)) * 100

        # Ajouter les pourcentages totaux au contexte
        context['club_percentage_total'] = club_percentage_total
        context['shop_percentage_total'] = shop_percentage_total
        print(context['shop_percentage_total'])
        return context
    

    
    
    

class ContactView(SuccessMessageMixin, CreateView):
    template_name = 'public/contact.html'
    model = Contact
    form_class = ContactForm
    success_message = _(
        "Your subject is registered, Our support team will contact you in the brief date")
    success_url = reverse_lazy('contact')

    def form_valid(self, form, *args, **kwargs):

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        message = form.cleaned_data['message']
        subject = form.cleaned_data['subject']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        email = form.cleaned_data['email']

        subject, from_email, to = subject, email, "linayousfi09@gmail.com"
        text_content = _(
            f'Hello Team <br> <p>Mr/Ms: <strong>{first_name} {last_name}</strong> need help about <strong> {subject} </strong> <br> His/Her message:<br> {message} </p> <p><a href="mailto:{email}">Reply to customer email</a></p>')
        html_content = _(
            f'Hello Team <br> <p>Mr/Ms: <strong>{first_name} {last_name}</strong> need help about <strong> {subject} </strong> <br> His/Her message:<br> {message} </p> <p><a href="mailto:{email}">Reply to customer email</a></p>')
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return super().form_valid(form)


class PagesView(DetailView):
    model = Page
    template_name = 'public/page.html'


def page_not_found_view(request, exception):
    template_name = 'error/404.html'
    return render(request, template_name, status='404')


def error_view(request):
    template_name = 'error/500.html'
    return render(request, template_name, status='500')


def permission_denied_view(request, exception):
    template_name = 'error/403.html'
    return render(request, template_name, status='403')


def bad_request_view(request, exception):
    template_name = 'error/400.html'
    return render(request, template_name, status='400')


class RobotTxt(TemplateView):
    template_name = 'components/robots.txt'



def your_view(request):
    return render(request, 'public/chart.html')
