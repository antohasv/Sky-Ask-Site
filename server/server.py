from twisted.internet import reactor, task
from twisted.web.resource import Resource
from twisted.web import server
import MySQLdb as mysql
from conf import DATABASES
import datetime
import json

class SkyQstServer(Resource):
	isLeaf = True
	
	def __init__(self):
		sec = 5
		
		self.delayed_requests = []
		
		loop = task.LoopingCall(self.delayRequest)
		loop.start(sec)
		Resource.__init__(self)
		
	def format(self, rows):
		s = ""
		for row in rows:
			s += '{{"id":"{0}", "content":"{1}", "qst_id":"{2}", "user_id":"{3}", "date":"{4}", "flag":"{5}", "raiting":"{6}"}},'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
		s = s[0:-1]
		res = '{{"status": "ok","res":[{0}]}}'.format(s)
		return 'server({0});'.format(res);
			
		
	def getData(self, qst_id, asw_id):
		try:
			con = mysql.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['DB'])
			cur = con.cursor()
			n = cur.execute('select * from `ask_answer` where `qst_id` = {0} and id > {1}'.format(qst_id, asw_id))
			
			if n == 0:
				return ""
			
			rows = cur.fetchall()
			return rows
		except mysql.Error:
			return ""
		
	def render(self, request):
		args = request.args
		request.setHeader('Content-Type', 'application/json')
		
		#Question and Last answer Id:
		if not 'asw' in args or not 'qst' in args:
			res = json.dumps({'status': 200, 'code' : '1'})
			res = 'server({0});'.format(res);
			return res #"Write GET parameters: qst_id and asw_id
			
		try:
			qst_id = int(args['qst'][0])
			asw_id = int(args['asw'][0])
		except:
			res = json.dumps({'status': "error", 'code' : '1'})
			res = 'server({0});'.format(res);
			return res #"Write GET parameters: qst_id and asw_id
			
		print "\n" + ("=" * 50) 
		print "[Server]SkyQst: Connect\nQst_Id:{0} \nLast Asw_Id: {1}".format(qst_id, asw_id) 
		print ("=" * 50) + "\n" 
		
		data = self.getData(qst_id, asw_id)
		if len(data) > 0:
			print "\n" + ("=" * 50) 
			print "[Server]SkyQst: SendData\nQst_Id:{0} \nLast Asw_Id: {1}\nSend data\n{2}".format(qst_id, asw_id, str(data)) 
			print ("=" * 50) + "\n" 
			return self.format(data);
			
		self.delayed_requests.append(request)
		
		return server.NOT_DONE_YET
		
	def delayRequest(self):
		for request in self.delayed_requests:
			if request._disconnected == False:
				qst_id = int(request.args['qst'][0])
				asw_id = int(request.args['asw'][0])
				data = self.getData(qst_id, asw_id)
				if len(data) > 0:
					try:
						print "\n" + ("=" * 50) 
						print "[Server]SkyQst: SendData\nQst_Id:{0} \nLast Asw_Id: {1}\nSend data\n{2}".format(qst_id, asw_id, str(data)) 
						print ("=" * 50) + "\n" 
						request.write(self.format(data))
						request.finish()
					except:
						print "Fatal Error: in delay Request."
					finally:
						self.delayed_requests.remove(request)
			else:
				self.delayed_requests.remove(request)

def main():
	port = 8081
	site = server.Site(SkyQstServer())
	reactor.listenTCP(port, site)
	print "[Server]SkyQst: Start."
	reactor.run()

if __name__ == "__main__":
	main()
