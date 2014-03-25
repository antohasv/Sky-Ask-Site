from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String

class Question(Base):
	__tablename__ 'ask_question'
	
	id = Column(Integer, primary_key = True)
	title = Column(String(60))
	content = Column(String)
	topic_id = Column(Integer, ForeignKey(''))
	user_id = models.ForeignKey(User)
	date = models.DateField()
	raiting = models.IntegerField()
