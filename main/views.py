from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from .models import Stock 

# def index(request):
# 	latest_question_list = Stock.objects.order_by('date')[:10]
# 	template = loader.get_template('main/index.html')
# 	context = {
# 		'latest_question_list': latest_question_list,
# 	}
# 	return HttpResponse(template.render(context, request))

def search(request):
	template = loader.get_template('main/index.html')

	if request.method == 'GET':
		return HttpResponse(template.render(None, request))


	symbol = request.POST.get("stock_symbol")

	try:
		start = datetime.strptime(request.POST.get("start_date"), "%d/%m/%Y").date()
		end = datetime.strptime(request.POST.get("end_date"), "%d/%m/%Y").date()
	except ValueError as err:
		context = {
			'error' : True
		}
		return HttpResponse(template.render(context, request))


	if not isValid(symbol, start, end):
		context = {
			'error' : True
		}
		return HttpResponse(template.render(context, request))

	latest_point_list = Stock.objects.order_by('date').filter(stock_symbol=symbol).exclude(date__lt=start).exclude(date__gt=end)
	labels = [None] * len(latest_point_list)
	prices = [None] * len(latest_point_list)
	count = 0

	
	for point in latest_point_list:
		labels[count] = point.date.strftime("%m/%d/%Y")
		prices[count] = int(point.close_price)
		count += 1

	context = {
		'code_name' : symbol,
		'start_date': request.POST.get("start_date"),
		'end_date': request.POST.get("end_date"),
		'labels' : labels,
		'prices' : prices
	}
	return HttpResponse(template.render(context, request))



def isValid(symbol, start_date, end_date):
	supported_codes = ["APPL", "CSCO", "INTC", "MSFT"]

	return symbol in supported_codes and start_date < end_date

