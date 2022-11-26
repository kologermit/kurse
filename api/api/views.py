from django.http import HttpResponse
from DB import DB
import json
import logging
database = DB(postgres = {
	"user": "master",
	"password": "masterPassword",
	"host": "postgres",
	"dbname": "hostel",
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


def select(request):
	try:
		res = params_verification(request.GET, ["table", "columns", "where"])
		params_dict = dict(request.GET)
		if res != True:
			return error_return(res)
		columns = json.loads(params_dict["columns"][0])
		result = [{columns[j]: i[j] for j in range(len(columns))} for i in database.select(table=params_dict["table"][0],
			columns=columns, 
			where=json.loads(params_dict["where"][0]), 
			limit=params_dict.get("limit", [""])[0],
			is_print_sql_query=(params_dict.get("is_print_sql_query", ["False"])[0].upper() == "TRUE"))]
		return success_return(result)
	except Exception as err:
		logging.error(err)
		return error_return(str(err))

def update(request):
	try:
		res = params_verification(request.GET, ["table", "values", "where"])
		params_dict = dict(request.GET)
		if res != True:
			return error_return(res)
		result = database.update(table=params_dict["table"][0],
			values=json.loads(params_dict["values"][0]), 
			where=json.loads(params_dict["where"][0]), 
			is_print_sql_query=(params_dict.get("is_print_sql_query", ["False"])[0].upper() == "TRUE"),
			return_count=True)
		return success_return({"count_updated": result[0][0]})
	except Exception as err:
		logging.error(err)
		return error_return(err)

def insert(request):
	try:
		res = params_verification(request.GET, ["table", "columns", "values"])
		params_dict = dict(request.GET)
		if res != True:
			return error_return(res)
		result = database.insert(table=params_dict["table"][0],
			values=json.loads(params_dict["values"][0]), 
			columns=json.loads(params_dict["columns"][0]), 
			is_print_sql_query=(params_dict.get("is_print_sql_query", ["False"])[0].upper() == "TRUE"),
			lastval=(params_dict.get("lastval", ["False"])[0].upper() == "TRUE"))
		return success_return(result)
	except Exception as err:
		logging.error(err)
		return error_return(str(err))

def delete(request):
	try:
		res = params_verification(request.GET, ["table", "where"])
		params_dict = dict(request.GET)
		if res != True:
			return error_return(res)
		result = database.delete(table=params_dict["table"][0],
			where=json.loads(params_dict["where"][0]), 
			is_print_sql_query=(params_dict.get("is_print_sql_query", ["False"])[0].upper() == "TRUE"),
			return_count=True)
		return success_return({"count_deleted": result[0][0]})
	except Exception as err:
		logging.error(err)
		return error_return(str(err))

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