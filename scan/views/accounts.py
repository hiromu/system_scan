# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

def login(request):
    if request.user.is_authenticated():
        return redirect('scan.views.index')
    else:
        return django_login(request, 'accounts/login.html')

@login_required
def profile(request):
    return render_to_response('accounts/profile.html', context_instance=RequestContext(request))
