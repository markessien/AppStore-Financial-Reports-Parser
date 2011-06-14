import os
import glob

app_list = []
cur_rate = {}

EARNED_INDEX = 7
COPIES_SOLD_INDEX = 5
CURRENCY_INDEX = 8
NAME_INDEX = 12
APPID_INDEX = 10

class AppInfo:
	 def __init__(self):
		self.app_id = ""
		self.app_name = ""
		self.app_count = 0
		self.app_refund = 0
		self.app_sales_values = 0.0
		self.app_refunds_value = 0.0
		
def process():
	path = 'files/'
	for infile in glob.glob( os.path.join(path, '*.txt') ):
		print "Processing: " + infile
		fd = open(infile)
		content = fd.readline()
		while (content != "" ):
			content = fd.readline()
			process_line(content)
	
	print "######\nProcessed " + len(app_list).__str__() + " apps::::"
	for app in app_list:
		print "-- " + app.app_name + ". " + app.app_count.__str__() + " copies sold " + " for $" + str(app.app_sales_values)
	print "Done!"

def process_line(line):
	items = line.split("\t")
	if len(items) < 3:
		return
	
	app = find_or_create_app(items[APPID_INDEX])
	app.app_name = items[NAME_INDEX]
	
	copies_sold = long(items[COPIES_SOLD_INDEX])
	app.app_count = app.app_count + copies_sold
	app.app_sales_values = app.app_sales_values + convert_currency(items[EARNED_INDEX], items[CURRENCY_INDEX])
	# print "Read:" + items[CURRENCY_INDEX]

def convert_currency(val, cur):
	if cur == "USD":
		return float(val)
		
	if cur_rate.has_key(cur) == False:	
		rate = download_exchange_rate(cur)
		cur_rate[cur] = rate
		print "Rate for " + cur + " to USD=" + str(rate)
	
	return float(val) * cur_rate[cur]
	
def download_exchange_rate(currency):
		url = "http://download.finance.yahoo.com/d/quotes.csv?s=" + currency + "USD=X&f=l1"
		import urllib2
		req = urllib2.Request(url=url)
		response = urllib2.urlopen(req)
		data = response.read()
		return float(data)
		
def find_or_create_app(app_id):
	for app in app_list:
		if app.app_id == app_id:
			return app
			
	# App not found
	app = AppInfo()
	app.app_id = app_id
	app_list.append(app)
	return app
	
process()