from django.urls import path
from public import views
from public.views import MyChartView
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    path('chart/', MyChartView.as_view(), name='chart'),
    path('<slug:slug>/', views.PagesView.as_view(), name='page'),
    
]
