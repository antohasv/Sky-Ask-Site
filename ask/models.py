#-*- coding:utf-8 -*-
from django.db import models

class User(models.Model):
	name = models.CharField(max_length = 30)
	email = models.EmailField()
	password = models.CharField(max_length = 40)
	reg_date = models.DateField()
	raiting = models.IntegerField(blank = True)
	
	def __unicode__(self):
		return "%s" % self.name


class Topic(models.Model):
	name = models.CharField(max_length = 50)
	
	def __unicode__(self):
		return "%s" % self.name

		
class Question(models.Model):
	title = models.CharField(max_length = 60)
	content = models.TextField()
	topic = models.ForeignKey(Topic)
	user = models.ForeignKey(User)
	date = models.DateField()
	raiting = models.IntegerField()
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ['date']
	
class Answer(models.Model):
	content = models.TextField()
	qst = models.ForeignKey(Question)
	user = models.ForeignKey(User)
	date = models.DateField()
	flag = models.BooleanField()
	raiting = models.IntegerField()
	
	def __unicode__(self):
		return self.content
		
class QstLikes(models.Model):
	qst = models.ForeignKey(Question)
	user = models.ForeignKey(User)
	
	def __unicode__(self):
		return "Question: {0} User: {1}".format(self.qst.id, self.user.name)
		
class AswLikes(models.Model):
	asw = models.ForeignKey(Answer)
	user = models.ForeignKey(User)
	
	def __unicode__(self):
		return "Question: {0} User: {1}".format(self.asw.id, self.user.name)

class QComments(models.Model):
	content = models.TextField()
	date = models.DateField()
	user = models.ForeignKey(User)
	qst = models.ForeignKey(Question)
	
	def __unicode__(self):
		return "Comment_id:{0} User_id:{1} Question_id:{2}".format(self.id, self.user.id, self.qst.id)
		
class AComments(models.Model):
	content = models.TextField()
	date = models.DateField()
	user = models.ForeignKey(User)
	asw = models.ForeignKey(Answer)
	
	def __unicode__(self):
		return "Comment_id:{0} User_id:{1} Answer_id:{2}".format(self.id, self.user.id, self.asw.id)
