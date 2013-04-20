from django.http import HttpResponse

def render_to_disabled(request):
	return HttpResponse("Stiamo apportando nuovi aggiornamenti!")