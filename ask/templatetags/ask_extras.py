from django import template
from ask.models import Question, User

register = template.Library()

#Answer cout
@register.filter(name = 'acout')
def acout(value):
	return value.answer_set.all().count()
	
#Get name By Id
@register.filter(name = 'get_name')
def get_name(value):
	id = int(value)
	try:
		u = User.objects.get(id = id)
	except User.DoesNotExist:
		return "UnKnown"
	return u.name
