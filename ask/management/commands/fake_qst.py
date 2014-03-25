from django.core.management.base import BaseCommand, CommandError
from ask.models import Question, User, Topic
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
		for i in range(1, n):
			title = self.fake.text(random.randint(10, 40))
			content = self.fake.text(random.randint(500, 1500))
			topic = Topic.objects.get(id = int(random.randint(1, Topic.objects.count())))
			user = User.objects.get(id = int(random.randint(1, User.objects.count())))
			date = self.fake.rdate()
			q = Question(title = title, content = content, topic = topic, user = user, date = date)
			q.save()
