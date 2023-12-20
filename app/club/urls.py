from django.urls import path
from club import views

urlpatterns = [
    path('organizer/<str:username>/create-club/', views.CreateClubView.as_view(), name='create-club'),
    path('organizer/<str:username>/update-club/<slug:slug>/', views.UpdateClubView.as_view(), name='update-club'),
    path('organizer/<str:username>/delete-club/<slug:slug>/', views.DeleteClubView.as_view(), name='delete-club'),
    path('clubs/', views.ListClubView.as_view(), name='list-club'),
    path('club/<slug:slug>/', views.ClubView.as_view(), name='club'),
]
