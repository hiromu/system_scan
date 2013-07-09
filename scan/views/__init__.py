# -*- coding: utf-8 -*-

from scan.models import Contest

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    contest_list = Contest.objects.all().order_by('-start')

    context = {'contest_list': contest_list}
    return render_to_response('index.html', context, RequestContext(request))
