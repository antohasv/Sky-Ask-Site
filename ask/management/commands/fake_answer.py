from django.core.management.base import BaseCommand, CommandError
from ask.models import Question, User, Answer
from fake import Fake
import random

	
class Command(BaseCommand):
	args = '< n >'
	help = 'Write how many data do you want to add'
	
	def __init__(self):
		self.fake = Fake()
		
		for i in range(1, 10):
			self.fake.arr.append(' ')
		
	def handle(self, *args, **options):
		n = int(args[0])
		qn = Question.objects.count()
		qu = User.objects.count()
		for i in range(1, n):
			user = User.objects.get(id = random.randint(1, qu))
			try:
				a = Answer(content = self.fake.text(random.randint(50, 400)), qst = Question.objects.get(id = random.randint(1, qn)), 
									user = user, date = self.fake.date(user.reg_date.month, user.reg_date.year), flag = False, raiting=0)
				a.save()
			except Question.DoesNotExist:
				print("Question does not exist")
