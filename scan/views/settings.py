# -*- coding: utf-8 -*-

from scan.forms.settings import *
from scan.models import Contest

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

@login_required
def index(request):
    if not request.user.is_staff:
        return redirect('scan.views.index')

    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = form.save()
            return redirect('scan.views.settings.contest', contest_id = contest.id)
    else:
        form = ContestForm()

    context = {'form': form}
    return render_to_response('settings/index.html', context, RequestContext(request))

@login_required
def problem(request, contest_id, genre_id):
    return redirect('scan.views.index')
