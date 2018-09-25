from sanic import Sanic
from sanic.response import json,text
import pymongo
import random

app = Sanic()

@app.route('/ip',methods=['GET'])
async def getIp(request):
	u = request.args['u'][0]
	p = request.args['p'][0]
	print(u,p)
	if u == 'nathaniel' and p == '458656120':
		client = pymongo.MongoClient('127.0.0.1',27017)
		db = client['tool']
		collect = db['ip']
		data = collect.find()[random.randint(0,10)]
		client.close()
		return json({'http':data['http'],'ip':data['ip'],'port':data['port']})
	return text('sorry')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=9000)