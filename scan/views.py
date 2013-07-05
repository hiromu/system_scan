# Create your views here.
from system_scan.scan.models import *
from django.http import HttpResponse
from django.template import Context, loader

def index(request):
	contest_list = Contest.objects.all().order_by('-start')

	template = loader.get_template('index.html')
	context = Context({'contest_list': contest_list})
	return HttpResponse(template.render(context))

