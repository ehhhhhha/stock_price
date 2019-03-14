from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from .models import Stock 
import json



# for simplicity, this function will handle both GET and POST request 
def search(request):
	template = loader.get_template('main/index.html')

	# for GET request just return empty template page
	if request.method == 'GET':
		return HttpResponse(template.render(None, request))


	# retrieve form input  
	symbol = request.POST.get("stock_symbol")

	# validate datetime format 
	try:
		start = datetime.strptime(request.POST.get("start_date"), "%d/%m/%Y").date()
		end = datetime.strptime(request.POST.get("end_date"), "%d/%m/%Y").date()
	except ValueError as err:
		context = {
			'error' : True
		}
		return HttpResponse(template.render(context, request))

	# validate stock symbol and datetime order
	if not isValid(symbol, start, end):
		context = {
			'error' : True
		}
		return HttpResponse(template.render(context, request))

	# query database and retrieve data
	latest_point_list = Stock.objects.order_by('date').filter(stock_symbol=symbol).exclude(date__lt=start).exclude(date__gt=end)
	labels = [None] * len(latest_point_list)
	prices = [None] * len(latest_point_list)
	count = 0

	# initialise label list and price data list for the chart 
	for point in latest_point_list:
		labels[count] = point.date.strftime("%d/%m/%Y")
		prices[count] = int(point.close_price)
		count += 1


	# find the max profit and the dates
	length = len(prices)
	min_date_index = 0
	temp_min_date_index = 0 
	max_profit = 0
	max_profit_index = 0
	for i in range(length):
		if prices[temp_min_date_index] > prices[i]:
			temp_min_date_index = i
		if prices[i] - prices[temp_min_date_index] > max_profit:
			max_profit = prices[i] - prices[temp_min_date_index]
			max_profit_index = i
			min_date_index = temp_min_date_index

	# initialise a list of price for the max profit red line in the chart
	max_profit_point = [None] * length
	for i in range(length):
		if i >= min_date_index and i <= max_profit_index:
			max_profit_point[i] = prices[i]

	print(prices[min_date_index], prices[max_profit_index])
	max_profit_point = json.dumps(max_profit_point)

	# pass all valid data to view
	context = {
		'code_name' : symbol,
		'start_date': request.POST.get("start_date"),
		'end_date': request.POST.get("end_date"),
		'labels' : labels,
		'prices' : prices,
		'max_profit_point' : max_profit_point,
		'max_profit': max_profit,
		'max_profit_start': labels[min_date_index],
		'max_profit_end': labels[max_profit_index]
	}
	return HttpResponse(template.render(context, request))



# check code symbol and date order
def isValid(symbol, start_date, end_date):
	supported_codes = ["AAPL", "CSCO", "INTC", "MSFT"]
	return symbol in supported_codes and start_date < end_date

