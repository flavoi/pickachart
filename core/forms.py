from django.forms import *
from models import *

class ChartForm(ModelForm):
	class Meta:
		model = Chart
		exclude = ('author','volume')
		
class PieceForm(ModelForm):
	def __init__(self,user,*args,**kwargs):
		super(PieceForm,self ).__init__(*args,**kwargs)
		self.fields['chart'].queryset = Chart.objects.filter(author = user)
	class Meta:
		model = Piece
		exclude = ('author')
		
class ValuesForm(Form):
	yvalues = CharField(help_text = 'Valori Asse Y', widget = widgets.Textarea())
	labels = CharField(required=False, help_text = 'Etichette', widget = widgets.Textarea())
	def clean_yvalues(self):
		yvalues = self.cleaned_data["yvalues"].split(' ')
		try:
			for value in yvalues:
				float(value)
		except ValueError:
			raise ValidationError("Questi valori possono essere solo numeri!")
		return self.cleaned_data["yvalues"]
	