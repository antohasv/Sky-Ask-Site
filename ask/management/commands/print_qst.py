from django.core.management.base import BaseCommand, CommandError
from ask.models import Question, Users

class Command(BaseCommand):
	args = '< qst_id qst_id >'
	help = 'Fill table of questions'
	
	def handle(self, *args, **options):
		for qst_id in args:
			try:
				qst = Question.objects.get(id=int(qst_id))
			except Question.DoesNotExist:
				raise CommandError('Qst %s does not exist' % qst_id)
		#qst.save()
		try:
			user = Users.objects.get(id=int(qst.user.id))
		except Users.DoesNotExist:
			raise CommandError('Qst %s does not exist' % qst_id)
		
		
		self.stdout.write("Title: %s | User: %s | Date: %s\n" % (qst.title, user.name, qst.date))
