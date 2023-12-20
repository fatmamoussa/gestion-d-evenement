from django.urls import path
from event import views

urlpatterns = [
    path('organizer/<str:username>/create-event/', views.CreateEventView.as_view(), name='create-event'),
    path('organizer/<str:username>/update-event/<slug:slug>/', views.UpdateEventView.as_view(), name='update-event'),
    path('organizer/<str:username>/delete-event/<slug:slug>/', views.DeleteEventView.as_view(), name='delete-event'),
    path('events/', views.ListEventView.as_view(), name='list-event'),
    path('event/<slug:slug>/', views.EventView.as_view(), name='event'),#path detail event
    path('event/detail/<slug:slug>/like/', views.likes, name='like_event'),
    # path('event/<int:comment_id>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('event/<slug:slug>/subscribers/', views.SubscribersView.as_view(), name='subscribers'),#path liste subscribers
    # path('event/<slug:event_slug>/update_comment/<int:comment_id>/', views.EventView.as_view(), name='event_update_comment'),
    # path('event/<slug:slug>/update_comment/<int:pk>/', views.UpdateCommentView.as_view(), name='update_comment'),







]