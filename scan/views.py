# Create your views here.
from system_scan.scan.models import *

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
