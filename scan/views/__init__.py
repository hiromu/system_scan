# -*- coding: utf-8 -*-

from scan.models import Contest

from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

def index(request):
    contest_list = Contest.objects.all().order_by('-start')
    contests_in_progress = []
    scheduled_contests = []
    now = timezone.now()
    for contest in contest_list:
        if now < contest.start:
            scheduled_contests.append(contest)
        elif now < contest.end:
            contests_in_progress.append(contest)

    context = {'contest_list': contest_list, 'contests_in_progress': contests_in_progress, 'scheduled_contests': scheduled_contests, 'now': now}
    return render(request, 'index.html', context)
