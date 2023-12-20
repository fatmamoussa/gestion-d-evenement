from django.urls import path
from connection import views
urlpatterns = [
    path('accounts/profile/<str:username>/',views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/<str:username>/settings/',views.profileSettings, name='settings'),#update profilee
]
