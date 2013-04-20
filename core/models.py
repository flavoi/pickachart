from django.db import models

# Create your models here.
class ProtModel(models.Model):
	author = models.ForeignKey('auth.User')
	class Meta:
		abstract = True
		
class Chart(ProtModel):
	title = models.CharField(max_length=100, verbose_name="titolo")
	volume = models.PositiveIntegerField(null = True, blank = True, verbose_name="numero di dati") # <-- deprecated
	style = models.CharField(max_length=30, verbose_name="stile", choices=(('lc','Grafico a Linee'),('bvg','Grafico a Barre'),('mst','Grafico misto Barre/Linea')))
	width = models.CharField(max_length=10, verbose_name="dimensione", choices=(('380x225','Piccolo'),('420x335','Medio')))
	color = models.CharField(verbose_name="colore", max_length=6, choices=(('A2C180','Verde'),('3072F3','Azzurro'),('EE9918', 'Arancio'),('0000FF','Blu'),('990066','Viola'), ('C2BDDD','Violetto')))
	grid = models.CharField(blank=True, null=True, verbose_name="griglia", max_length=20, choices=(('&chg=5,0','Orizzontale'),('&chg=0,5','Verticale'),('&chg=5,5','Completa')))
	scale_to = models.PositiveIntegerField(null = True, blank = True, verbose_name="Scala Max")
	def __unicode__(self):
		return u"%s" % (self.title)
	class Meta:
		verbose_name_plural= "Charts"

class Piece(ProtModel):
	value = models.FloatField(verbose_name="valore y")
	label = models.CharField(blank=True, null=True, verbose_name="etichetta", max_length=15)
	chart = models.ForeignKey(Chart, verbose_name="Grafico")
	def __unicode__(self):
		return u"%s %s" % (self.value, self.label)