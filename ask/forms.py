from django import forms

class UserForm(forms.Form):
	name = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField()
	reg_date = forms.DateField()

class EnterForm(forms.Form):
	name = forms.CharField()
	password = forms.CharField()

class RegForm(forms.Form):
	name = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField()
	
class AskForm(forms.Form):
	title = forms.CharField()
	content = forms.CharField()
	topic = forms.IntegerField()
