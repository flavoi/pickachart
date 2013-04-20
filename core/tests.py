from django.shortcuts import render_to_response
from django.template import RequestContext

def simpleTest(request):
	return HttpResponse("test")
   	#return render_to_response('allcharts.html', RequestContext(request))

