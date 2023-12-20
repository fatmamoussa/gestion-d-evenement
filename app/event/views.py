from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, DetailView, CreateView, ListView, UpdateView, TemplateView
from django.views.generic.edit import ModelFormMixin, FormMixin
from event.forms import EventForm, CommentForm, CommentDeleteForm
from shop.models import Shop
from event.models import Event, Comment
from club.models import Club
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.signals import notify
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.views import View
from datetime import datetime
from datetime import date


class CreateEventView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    # la classe de formulaire
    form_class = EventForm
    template_name = "event/index.html"
    # message de succès lorsqu'un nouvel événement est créé.
    success_message = _("%(name)s was created successfully")

    def form_valid(self, form):
        # l'utilisateur actuellement connecté (self.request.user)
        form.instance.user = self.request.user
        club_or_shop_value = form.cleaned_data.get('club_or_shop')
# startswith()  Elle permet de vérifier si une chaîne commence par club alors elle envoie true
        if club_or_shop_value.startswith('club_'):
            # elle divise les chaine par _
            club_id = club_or_shop_value.split('_')[1]
            # recupere id de club a travers la base de donnee
            club = Club.objects.get(pk=club_id)

            form.instance.club = club
        elif club_or_shop_value.startswith('shop_'):
            shop_id = club_or_shop_value.split('_')[1]
            shop = Shop.objects.get(pk=shop_id)
            form.instance.shop = shop
            # permet d'enregistrer form dans la base de donne en cas de validiter

        return super().form_valid(form)

    def get_form_kwargs(self):
        # recuper les attribus dans un variable kwargs
        kwargs = super().get_form_kwargs()
        # determiner le userr connecter
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # recupere tout les objects dans un selue form
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all().order_by('event_date')[:1]

        return context


class UpdateEventView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event/index.html"
    success_message = _("%(name)s was updated successfully")
    # renvoi l obj specifique

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # si le utilisateur n'est pas la createur de l'event
        if not obj.user == self.request.user:
            # l'utilisateur n'est pas autorisé à y accéder.
            raise Http404
        # l'utilisateur est autorisé à accéder
        return obj
# cette methode appeler lorsque le form valide

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.request.user
        # Cela retourne l'objet créé, mais ne l'enregistre pas encore car commit =false
        obj = form.save(commit=False)
        if not obj.user == self.request.user:
            messages.error(
                self.request, "You are not authorized to update this event.")
            return redirect('event', slug=obj.slug)
        # lobjet est enregistrer
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs




class DeleteEventView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        created_date = event.event_date

        if created_date and created_date < date.today():
            messages.error(self.request, _("Vous ne pouvez pas supprimer un événement dont la date est déjà passée."))
            return redirect(self.success_url)

        messages.success(self.request, _("Votre événement a été supprimé."))
        return super().delete(request, *args, **kwargs)
    
class ListEventView(ListView):
    model = Event
    template_name = "event/list.html"
    # nombre maximum dans la liste 10
    paginate_by = 10

class EventView(DetailView):
    model = Event
    template_name = 'event/event.html'
    comments_per_page = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        comments = Comment.objects.filter(event=event).order_by('-created_on')

        total_likes = event.total_likes()
        liked = False
        if event.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        context["form"] = CommentForm()
        context["comments"] = comments
        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]
        context["comments_count"] = comments.count()
        return context

    def delete_comment(self, comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()

    def update_comment(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)

        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect(self.request.path)
        else:
            form = CommentForm(initial={'message': comment.message})

        return render(request, 'event/_comment_update.html', {'form': form, 'comment_id': comment_id})

    def post(self, request, *args, **kwargs):
        if 'delete_comment_id' in request.POST:
            comment_id = int(request.POST.get('delete_comment_id'))
            self.delete_comment(comment_id)
            return redirect(self.request.path)
        elif 'update_comment_id' in request.POST:
            comment_id = int(request.POST.get('update_comment_id'))
            return self.update_comment(request, comment_id)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.event = self.get_object()
                new_comment.save()
                event = get_object_or_404(Event, slug=self.get_object().slug)
                comment = form.cleaned_data['message']
                object_url = self.request.build_absolute_uri(
                    reverse('event', args=[self.get_object().slug]))
                if event.user == request.user:
                    sender = self.request.user
                    recipient = User.objects.filter(is_staff=False)
                    message = _(
                        f"A comment is added to the event {event.name} from the user {event.user.username} ")
                else:
                    sender = self.request.user
                    recipient = event.user
                    message = _(
                        f"A comment is added to the event {event.name} from the user {event.user.username} ")

                notify.send(
                    sender=sender,
                    recipient=recipient,
                    verb='Message',
                    description=mark_safe(comment),
                    url=object_url,
                    **kwargs
                )
        return redirect(self.request.path)


def likes(request, slug):
    # get_object_or_404 pour récupérer l'objet Event correspondant à l'ID envoyé via la méthode POST
    #  dans la clé 'object_id'. Si aucun objet correspondant n'est trouvé, une erreur 404 est renvoyée.
    event = get_object_or_404(Event, id=request.POST.get('object_id'))
    liked = False
    max_subscriber = event.max_subscriber
    if event.likes.count() >= max_subscriber:
        # Le nombre de likes a atteint ou dépassé le nombre d'abonnés
        messages.error(request, "Le nombre maximum de likes a été atteint.")
    else:
        # Cette ligne vérifie si l'utilisateur actuel a déjà aimé
        # l'événement en vérifiant si son ID est présent dans le champ likes de l'objet event
        if event.likes.filter(id=request.user.id).exists():
            event.likes.remove(request.user)
            liked = False
        else:
            event.likes.add(request.user)
            liked = True

    return HttpResponseRedirect(reverse('event', args=[str(slug)]))


# liste des participants dans chaque evenement
class SubscribersView(TemplateView,SuccessMessageMixin):
    
    template_name = "event/subscribers.html"
# Cette méthode est utilisée pour obtenir les données de contexte à passer au template lors de l'affichage de la vue
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ce paramètre correspond au slug de l'événement dont on souhaite afficher les abonnés.
        slug = kwargs['slug']
        # get_object pour récupérer l'objet Event associé au slug donné. Si aucun événement correspondant n'est trouvé, une erreur 404 est renvoyée.
        event = get_object_or_404(Event, slug=slug)
        # recupere tout les subscriber de l event
        subscribers = event.likes.all()
       # Cette liste sera disponible dans le template pour afficher les abonnés de l'événement.
        context['subscribers'] = subscribers
        context['event_name'] = event.name
        context['event_date'] = event.event_date.strftime('%d/%m/%Y')
        context['event_location'] = event.address

        context["shops"] = Shop.objects.all()[:1]
        context["clubs"] = Club.objects.all()[:1]
        context["events"] = Event.objects.all()[:1]

        return context
