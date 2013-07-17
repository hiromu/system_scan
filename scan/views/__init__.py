# -*- coding: utf-8 -*-

import datetime

from scan.models import Contest

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

def index(request):
    contest_list = Contest.objects.all().order_by('-start')
    for contest in contest_list:
        now = datetime.datetime.now()
        if now < contest.start:
            contest.state = _(u'あと%(period)sで開始') % {'period': (contest.start - datetime.datetime.now()) // 1000000 * 1000000}
        if now >= contest.start and now < contest.end:
            contest.state = _(u'開催中')
        if now >= contest.end:
            contest.state = _(u'終了')

    context = {'contest_list': contest_list}
    return render_to_response('index.html', context, RequestContext(request))
