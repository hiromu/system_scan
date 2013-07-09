# -*- coding: utf-8 -*-

from django.contrib.auth.views import login as django_login
from django.shortcuts import redirect

def login(request):
    if request.user.is_authenticated():
        return redirect('scan.views.index')
    else:
        return django_login(request, 'accounts/login.html')

def profile(request):
    return redirect('scan.views.index')
