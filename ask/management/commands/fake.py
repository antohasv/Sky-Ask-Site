import random
import calendar

class Fake:
	def __init__(self):
		self.first = [] # The first character
		self.arr = [] 
		
		for i in range(97, 123):
			self.first.append(chr(i))
			self.arr.append(chr(i))
			
		for j in range(0, 10):
			self.arr.append(j)
		self.arr.append('_')
		
		
	def text(self, n = 5):
		s = []
		s.append(random.choice(self.first))
		for i in range(1, n):
			s.append(str(random.choice(self.arr)))
		s.append(random.choice(self.first))
		return "".join(s)
		
	def rdate(self): # random date
		year = random.randint(2000, 2013)
		month = random.randint(1, 12)
		days = calendar.monthrange(year, month)
		d = "%s-%s-%s" % (year, month, random.randint(1, days[1]))
		return d
	
	def date(self, m, y):
		m = int(m)
		y = int(y)
		year = random.randint(y, 2013)
		
		if year == y:
			month = random.randint(m, 12)
		else:
			month = random.randint(1, 12)
			
		return "%s-%s-%s" % (year, month, random.randint(1, calendar.monthrange(year, month)[1]))
