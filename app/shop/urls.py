from django.urls import path
from shop import views
urlpatterns = [
    path('organizer/<str:username>/create-shop/', views.CreateShopView.as_view(), name='create-shop'),
    path('organizer/<str:username>/update-shop/<slug:slug>/', views.UpdateShopView.as_view(), name='update-shop'),
    path('organizer/<str:username>/delete-shop/<slug:slug>/', views.DeleteShopView.as_view(), name='delete-shop'),
    path('shops/', views.ListShopView.as_view(), name='list-shop'),
    path('shop/<slug:slug>/', views.ShopView.as_view(), name='shop'),
]
