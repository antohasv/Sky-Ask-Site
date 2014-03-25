from django.core.management.base import BaseCommand, CommandError
from ask.models import Topic
import random

class Command(BaseCommand):
	args = '< n >'
	help = 'Write how many data do you want to add'
	
	def __init__(self):
		self.topics = ["C/C++","Java","Python","Perl","Android","IOS","PHP","Javascript","JQuery","AJAX","Linux","Windows","C#","F#","Cobol",
							"Mysql","Sql","Asp.net","Objective-c","Django","Html5","Css","Ruby","Database","Eclipse","Postgresql","Bash","Wpf","Json","Xcode","Oracle","Github","Matlab"]
        
	def handle(self, *args, **options):
		for  i in self.topics:
			t = Topic(name = i)
			t.save()
