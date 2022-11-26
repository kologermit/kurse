import requests
url = "http://localhost:9001/update/"
data = {
	"table": "clients",
	"values": '{"clientPrepayment": 11}',
	"where": '[{"column": "cliendId", "cond_sign": "=", "data": 1}]'
}
res = requests.get(url, data)
print(res.content.decode())