# -*- coding: utf-8 -*-

from system_scan.scan.forms import *

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

@login_required
def index(request):
	if not request.user.is_staff:
		return redirect('system_scan.scan.views.index')

	if request.method == 'POST':
		form = ContestForm(request.POST)
		if form.is_valid():
			contest = form.save()
			return redirect('system_scan.scan.views.settings.index', contest_id = contest.id)
	else:
		form = ContestForm()

	context = {'form': form}
	return render_to_response('setting.html', context, RequestContext(request))
