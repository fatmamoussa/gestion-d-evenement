
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.conf.urls import handler404
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve
from django.utils.translation import gettext_lazy as _
import notifications.urls
from public import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('superadmin_23/', admin.site.urls),
    path('robots.txt/', views.RobotTxt.as_view(), name='robots.txt'),#
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # Lorsqu'un utilisateur accède à une URL correspondante au modèle /media/..., le fichier correspondant sera servi à l'utilisateur.
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
    path('inbox/notifications/',
         include(notifications.urls, namespace='notifications')),
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += i18n_patterns(
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('connection.urls')),
    path('', include('shop.urls')),
    path('', include('club.urls')),
    path('', include('event.urls')),
    path('', include('public.urls')),
)
#la configuration des gestionnaires d'erreurs 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


handler404 = 'public.views.page_not_found_view'
handler500 = 'public.views.error_view'
handler403 = 'public.views.permission_denied_view'
handler400 = 'public.views.bad_request_view'

admin.site.site_header = "SuperAdmin Runner Out"
admin.site.site_title = "Runner Out"
admin.site.index_title = "Admin"
