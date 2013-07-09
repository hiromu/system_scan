# -*- coding: utf-8 -*-

from system_scan.scan.models import *
from system_scan.scan.forms import *

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    contest_list = Contest.objects.all().order_by('-start')

    context = {'contest_list': contest_list}
    return render_to_response('index.html', context, RequestContext(request))
