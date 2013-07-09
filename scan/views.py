# -*- coding: utf-8 -*-

from system_scan.scan.models import *
from system_scan.scan.forms import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import Context, RequestContext, loader

def index(request):
	contest_list = Contest.objects.all().order_by('-start')

	context = {'contest_list': contest_list}
	return render_to_response('index.html', context, RequestContext(request))

def custom_login(request):
	if request.user.is_authenticated():
		return redirect('system_scan.scan.views.index')
	else:
		return login(request, 'login.html')

@login_required
def setting(request):
	if request.method == 'POST':
		form = ContestForm(request.POST)
		if form.is_valid():
			contest = form.save()
			return redirect('system_scan.scan.views.setting_contest', contest_id = contest.id)
	else:
		form = ContestForm()

	context = {'form': form}
	return render_to_response('setting.html', context, RequestContext(request))
