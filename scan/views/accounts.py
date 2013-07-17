# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

def login(request):
    if request.user.is_authenticated():
        return redirect('scan.views.index')
    else:
        context = {'next': reverse('scan.views.index')}
        return django_login(request, 'accounts/login.html', extra_context = context)

@login_required
def profile(request):
    context = {'subtitles': [_(u'プロフィール')]}
    return render_to_response('accounts/profile.html', context, RequestContext(request))
