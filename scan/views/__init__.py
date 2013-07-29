# -*- coding: utf-8 -*-

import datetime

from scan.models import Contest

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

def index(request):
    contest_list = Contest.objects.all().order_by('-start')
    contests_in_progress = [];
    scheduled_contests = [];
    for contest in contest_list:
        now = datetime.datetime.now()
        if now < contest.start:
            scheduled_contests.append(contest)
        if now >= contest.start and now < contest.end:
            contests_in_progress.append(contest);

    context = {'contest_list': contest_list, 'contests_in_progress': contests_in_progress, 'scheduled_contests': scheduled_contests}
    return render_to_response('index.html', context, RequestContext(request))
