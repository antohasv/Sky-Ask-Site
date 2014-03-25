from django.core.management.base import BaseCommand, CommandError
from ask.models import User
import random
from fake import Fake
import hashlib

class Command(BaseCommand):
	args = '< n >'
	help = 'Write how many data do you want to add'

	def __init__(self):
		self.email = ["@mail.ru", "@gmail.com", "@rambler.ru", "@skyqst.com", "@yandex.ru", "@django.com"]
		self.fake = Fake()
		
	def handle(self, *args, **options):
		n = int(args[0])
		for i in range(1, n):
			uname = self.fake.text(random.randint(5, 13))
			eml = self.fake.text(random.randint(5, 13)) + random.choice(self.email)
			psd = hashlib.sha1(self.fake.text(random.randint(5, 13))).hexdigest()
			dt = self.fake.rdate()
			u = User(name = uname, email = eml, password = psd, reg_date = dt)
			u.save()
