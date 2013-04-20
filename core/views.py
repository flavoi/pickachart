from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Max

from forms import *
from models import *

@login_required
def viewall(request):
	charts = Chart.objects.filter(author=request.user).order_by('id').reverse()
	count = Chart.objects.filter(author=request.user).count()
	return render_to_response('allcharts.html', RequestContext(request, {'charts':charts, 'count':count}))

@login_required
def create_chart(request, idupdate=None, all=None):
	instance = None
	form = None
	if idupdate is not None:
		instance = Chart.objects.get(pk = int(idupdate))
		if instance.author != request.user:
			return HttpResponse(status=201)
	current_charts = None
	if request.user.is_superuser:
		current_charts = Chart.objects.all().order_by('id').reverse()[:5]
	else:
		current_charts = Chart.objects.filter(author=request.user).order_by('id').reverse()[:5]
	if request.method == 'POST':
		form = ChartForm(request.POST, instance = instance)
		if form.is_valid():
			chart = form.save(commit=False)
			chart.author = request.user
			chart.save()
			if idupdate:
				return HttpResponseRedirect(reverse('defdata',  args=[chart.id,idupdate]))
			return HttpResponseRedirect(reverse('defdata',  args=[chart.id,0]))
	else:
		#form vuoto iniziale
		form = ChartForm(instance = instance)
	return render_to_response('home.html', RequestContext(request, {'currents':current_charts, 'form':form, 'idupdate':idupdate}))

@login_required
def define_data(request, id, idupdate):
	if idupdate == '0':
		idupdate = None
	chart = Chart.objects.get(id = id)
	if chart.author != request.user:
		return HttpResponse(status=201)
	form = ChartForm(instance = chart)
	
	update_data = {'yvalues': '1 2 3', 'labels': 'a b c'}
	if idupdate:
		pieces = Piece.objects.filter(chart = chart)
		y = l = ''
		for p in pieces:
			y += str(p.value) + ' '
			l += str(p.label) + ' '
		y = y[:-1]
		l = l[:-1]
		update_data = {'yvalues': y, 'labels': l}
	form2 = ValuesForm(initial = update_data)
		
	if request.method == 'POST':
		form2 = ValuesForm(request.POST)
		if form2.is_valid():
			#elimino vecchi dati e reinserisco
			pieces = Piece.objects.filter(chart = chart)
			for p in pieces:
				p.delete()
			yvalues = (form2.cleaned_data['yvalues']).split(' ')
			labels = (form2.cleaned_data['labels']).split(' ')
			for y, l in zip(yvalues, labels):
				piece = Piece(author = request.user, value = float(y), label = l, chart = chart)				
				piece.save()
			return HttpResponseRedirect(reverse('visualize',  kwargs={'id':chart.id, 'style':chart.style}))
	return render_to_response('home.html', RequestContext(request, {'form':form,'form2':form2,'id':id,'idupdate':idupdate}))

		
@login_required	
def visualize_chart(request, id, style):
	#pulizia, elimino i grafici senza dati
	charts = Chart.objects.all()
	for c in charts:
		p = Piece.objects.filter(chart = c).count()
		if p == 0:
			c.delete()
	chart = Chart.objects.get(pk = int(id))
	#sicurezza get
	if chart.author != request.user:
		return HttpResponse(status=201)
	pieces = Piece.objects.filter(chart = chart)
	n_pieces = pieces.count()
	#costruzione url
	url = "http://chart.apis.google.com/chart?"
	dim = "&chs=%s" % chart.width
	color = "&chco=%s" % chart.color
	yvalues = "&chd=t:"
	for p in pieces:
		yvalues += "%s," % str(p.value)
	yvalues = yvalues[:-1]
	bar_option = "chxl=1:"
	for p in pieces:
		if p.label is not None:
			bar_option += "|%s" % p.label
	#se la scala non e' specificata viene impostata a max(value)
	if chart.scale_to:
		bar_option += "&chxr=0,0,%s" % chart.scale_to + "&chxt=y,x"
		scale = "&chds=0,%s" % chart.scale_to
	else: 
		max_value = pieces.aggregate(Max('value')).values()[0]
		bar_option += "&chxr=0,0,%s" % max_value + "&chxt=y,x" 
		scale = "&chds=0,%s" % str(max_value)
	type = "&cht=%s" % chart.style
	title = "&chtt=%s" % chart.title.replace(" ","+")
	cut = dim.find("x")
	width = dim[5:cut]
	height = dim[cut+1:]
	#in caso di griglia assente grid non vale None ma 'blank'
	grid = ''
	grid += str(chart.grid)
	url += bar_option + dim + type + color + scale + yvalues + grid + title
	if style == 'lc':
		url += "&chdlp=b&chls=2,4,1&chma=5,5,5,25&&chm=o,%s,0,-1,5" % chart.color
	if style == 'bvg':
		url += "&chbh=a"
	if style == 'mst':
		url += "&chm=B,C6D9FD,0,0,0|D,FF0000,0,0,4,1"
		url = url.replace("&cht=mst","&cht=bvg").replace(bar_option,"chbh=a&"+bar_option)
	url = url.replace('None', '')
	return render_to_response('home.html', RequestContext(request, {'data':chart, 'chart_url':url, 'chart_width':width, 'chart_height':height}))

