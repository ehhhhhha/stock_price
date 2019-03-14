from django.db import models

class Stock(models.Model):
	stock_symbol = models.CharField(max_length=10)
	close_price = models.DecimalField(max_digits=10, decimal_places=2)
	# to do: update() to fill later ?
	date = models.DateField()
	def __str__(self):
		return self.stock_symbol
		