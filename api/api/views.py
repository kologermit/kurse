from django.http import HttpResponse
from DB import DB
import json
import logging
import os
database = DB(postgres = {
	"user": os.environ.get('POSTGRES_USER'),
	"password": os.environ.get('POSTGRES_PASSWORD'),
	"host": os.environ.get('POSTGRES_HOST'),
	"dbname": os.environ.get('POSTGRES_DB'),
	"port": 5432
})

 
def error_return(message):
	return HttpResponse(json.dumps({"status": "ERROR", "message": message, "data": None}, indent=2))

def success_return(data):
	return HttpResponse(json.dumps({"status": "SUCCESS", "message": "OK", "data": data}, indent=2))

def params_verification(request, params):
	for i in params:
		if request.get(i) is None:
			return f"Parametr {i} not found"
	return True

def main(request):
	try:
		return success_return("Hostel")
	except Exception as err:
		logging.error(err)
		return error_return(err)

def query(request):
	try:
		res = params_verification(request.GET, ["query"])
		params_dict = dict(request.GET)
		if res != True:
			return error_return(res)
		result = database.query(params_dict["query"][0],
			isResult=(params_dict.get("is_result", ["False"])[0].upper() == "TRUE"))
		return success_return(result)
	except Exception as err:
		logging.error(err)
		return error_return(str(err))