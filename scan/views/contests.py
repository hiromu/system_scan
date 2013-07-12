# -*- coding: utf-8 -*-

from scan.forms.settings import *
from scan.models import Contest

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render_to_response, RequestContext

@login_required
def index(request, contest_id):
    contest = get_object_or_404(Contest, pk = contest_id)

    context = {'subtitles': [contest.name], 'contest_id': contest_id, 'genres': contest.genres.all(), 'users': contest.users.all()}
    return render_to_response('contests/index.html', context, RequestContext(request))

@login_required
def answer(request, contest_id, genre_id):
    return redirect('scan.views.index')
