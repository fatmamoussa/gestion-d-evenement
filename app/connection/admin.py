from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from connection.models import Activity, Profile

# afficher et éditer les profils utilisateur directement sur la page d'administration des utilisateurs. Cela facilite la gestion des profils associés aux utilisateurs.
class ProfileInline(admin.StackedInline):
    model = Profile
    #Cette ligne désactive la possibilité de supprimer un profil utilisateur en ligne.
    can_delete = False
    #la clé étrangère reliant le modèle Profile au modèle User est l'attribut user.
    fk_name = 'user'

#  personnaliser l'interface d'administration pour inclure le formulaire du profil utilisateur lors de la gestion des utilisateurs.
class ProfileUserAdmin(UserAdmin):
    #Cette ligne spécifie que la classe inline ProfileInline doit
    #  être incluse dans l'interface d'administration du modèle User.
    inlines = [ProfileInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(ProfileUserAdmin, self).get_inline_instances(request, obj)
#la classe user n est pas enregistere 
admin.site.unregister(User)
#la classe user et profile est enregisrter dans la meme page 
admin.site.register(User, ProfileUserAdmin,)
admin.site.register(Activity)


