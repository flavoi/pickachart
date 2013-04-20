from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.db import models

from models import *

'''gestione dei permessi
   un normale utente vede solo le proprie tabelle
   un superutente vede tutte le tabelle
'''
class ProtOption(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ProtOption, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author = request.user)
    
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser == False:
			obj.author = request.user
        obj.save()
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or obj.author == request.user:
            return True
        else:
            return False
    
    has_delete_permission = has_change_permission
	
		
class ChartOption(ProtOption):
	list_display = ('author','style','color','title','width')

class PieceOption(ProtOption):
	list_display = ('author', 'value','label','chart')
	
admin.site.register(Chart, ChartOption)
admin.site.register(Piece, PieceOption)