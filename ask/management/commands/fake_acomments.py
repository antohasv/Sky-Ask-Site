from django.core.management.base import BaseCommand, CommandError
from ask.models import Answer, User, AComments
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
		m = User.objects.all().count()
		an = Answer.objects.all().count()
		for i in range(1, n):
			try:
				asw  = Answer.objects.get(id = int(random.randint(1, an)))
				ac = AComments(content = self.fake.text(random.randint(50, 500)), date = self.fake.rdate(), user = User.objects.get(id = int(random.randint(1, m))), asw = asw)
				ac.save()
			except(User.DoesNotExist, Answer.DoesNotExist):
				print("No")
