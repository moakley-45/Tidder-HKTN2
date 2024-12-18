from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('home', views.HomePage.as_view(), name='home'),
]