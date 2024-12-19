from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from allauth.account.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

# Create your views here.


class HomePage(TemplateView):
    template_name = 'home/index.html'
