from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse,HttpResponseRedirect
from ask.models import User, Question, Answer, Topic, QstLikes, AswLikes
from django.shortcuts import render_to_response
from django.template import RequestContext
from ask.forms import EnterForm, RegForm, AskForm
import math, hashlib, datetime
from django.db.models import Max


#RightMenu
def get_topics():
	t = Topic.objects.all()
	return t
	
def get_users():
	u = User.objects.order_by("-reg_date")[0:10]
	return u
	
#Index.html(Page with qsts)
def index(req, page = 1):
	c = 20 # Number of items on the page
	page = int(page)
	lng = float(Question.objects.count())
	total = int(math.ceil(float(lng) / c)) # Number of pages (All pages)
	first_range = range(1, 6)
	last_range = range((total - 4),  (total + 1))
	
	if not 0 < page <= total:
		return HttpResponse("Page not found")
	
	sort = "date"
	if 'sort' in req.GET:
		sort = req.GET['sort']
		if sort == 'raiting':
			q = Question.objects.order_by("-raiting")[(page - 1) * 20 : (c * page - 1)]
			sort = "raiting"
		else:
			q = Question.objects.order_by("-date")[(page - 1) * 20 : (c * page - 1)]
	else:
		q = Question.objects.order_by("-date")[(page - 1) * 20 : (c * page - 1)]
	
	#Paginator 	
	has_prev = True
	has_next = True
	show_first = True
	show_last = True
	start = page - 3
	end = page + 4			
	
	if page == 1:
		has_prev = False
		page_numbers = first_range
	
	if page == total:
		has_next = False
		page_numbers = last_range
		
	if page in first_range:
		show_first = False
		start = 1
	
	if page in last_range:
		show_last = False
		end = total
	
 	paginator = {"has_prev": has_prev, "has_next": has_next, "current": page, "show_first": show_first, "show_last": show_last, 
					"pages": total, "page_numbers": range(start, end + 1), "prev" : (page - 1), "next": (page + 1)}	
 	d = {"qsts": q, "users": get_users(), "sname" : set_session(req), "topics": get_topics(), "users": get_users(), "sort": sort}
	return render_to_response("index.html", dict(d.items() + paginator.items()), context_instance = RequestContext(req))

#Question page(with Answers and Comments)	
def questions(req, qst_id):
	c = 30 # Visible columns on the page
	offset = 1 #  Number of the page
	right = False
	qst_id = int(qst_id)
	lng = float(Answer.objects.filter(qst = qst_id).count())
	total = int(math.ceil(float(lng) / c)) # Number of pages (All pages)
	first_range = range(1, 6)
	last_range = range((total - 4),  (total + 1))
	show_paginator = True
	
	if 'offset' in req.GET:
		offset = req.GET['offset']
		if offset:
			offset = int(offset)
			
	if offset > total:
		show_paginator = False 
			
	if qst_id > (Question.objects.all().count() + 10):
		 return HttpResponse(Question.objects.all().count())
	
	try:
		q = Question.objects.get(id = qst_id)
		max_asw = Answer.objects.filter(qst = q).aggregate(Max('id'))['id__max']
		a = Answer.objects.order_by("-flag", "-raiting", "-date").filter(qst = qst_id)[(offset - 1) * c : (offset * c -1)]
		r = Answer.objects.filter(qst = qst_id).filter(flag=1)
		if list(r) == []:
			if 'name' in req.session:
				if req.session['name']:
					if int(req.session['name']) == int(q.user.id):
						right = True 
			
	except (Question.DoesNotExist, Answer.DoesNotExist):
		return render_to_response("500.html");
	
	has_prev = True
	has_next = True
	show_first = True
	show_last = True
	start = offset - 3
	end = offset + 4			
	
	if offset == 1:
		has_prev = False
		page_numbers = first_range
	
	if offset == total:
		has_next = False
		page_numbers = last_range
		
	if offset in first_range:
		show_first = False
		start = 1
	
	if offset in last_range:
		show_last = False
		end = total 
	
 	paginator = {"show_paginator":show_paginator, "has_prev": has_prev, "has_next": has_next, "current": offset, "show_first": show_first, "show_last": show_last, 
					"pages": total, "page_numbers": range(start, (end + 1)), "prev" : (offset - 1), "next": (offset + 1)}	
	d = {"q" : q, "a" : a, "sname" : set_session(req), "users": get_users(), "topics": get_topics(), "right": right, "rightid": r, "max_asw": max_asw}			
	return render_to_response("qsts.html", dict(d.items() + paginator.items()), context_instance = RequestContext(req));	

def rightAnswer(req):
	id = ""
	if req.method == "POST":
		qid = req.POST["qid"]
		aid = req.POST["aid"]
		try:
			q = Question.objects.get(id = qid)
		except Question.DoesNotExist:
			return HttpResponse('{{"status":"error", "code":"{0}"}}'.format(3))
	else:
		return HttpResponse('{{"status":"error", "code":"{0}"}}'.format(2))
		
	if list(Answer.objects.filter(qst = qid).filter(flag=1)) == []:
			if 'name' in req.session:
				if req.session['name']:
					if int(req.session['name']) == int(q.user.id):
						try:
							a = Answer.objects.get(id = aid)
							a.flag = True
							a.save()
							return HttpResponse('{{"status":"ok", "id":"{0}"}}'.format(id))
						except Answer.DoesNotExist:
							return HttpResponse('{{"status":"error", "code":"{0}"}}'.format(1))
					else:
						return HttpResponse('{{"status":"error", "code":"{0}"}}'.format(2))
				else:
					return HttpResponse('{{"status":"error", "code":"{0}"}}'.format(3))
			else:
				return HttpResponse('{{"status":"error", "code":"{0}"}}'.format(4))
	return HttpResponse("Ok")

#Regestration
def regestration(req):
	return render_to_response("reg.html", {"users": get_users(), "topics": get_topics()}, context_instance = RequestContext(req))

#Enter
def enter(req):
	return render_to_response("enter.html", {"sname": set_session(req) ,"users": get_users(), "topics": get_topics()}, context_instance = RequestContext(req))

#Topics
def topics(req):
	t = Topic.objects.all()
	topics = [] 
	for i in t:	
		topics.append((i, i.question_set.all().count()))
	return render_to_response("topics.html", {"top": topics, "sname": set_session(req), "users": get_users(), "topics": get_topics()})

#User_INFO
def user_info(req, id):
	id = int(id)
	if id:
		try:
			u = User.objects.get(id = id)
			q = Question.objects.filter(user = u)
			a = Answer.objects.filter(user = u)
		except User.DoesNotExist:
			return HttpResponse("Error 404")
	return render_to_response("user.html",{"user":u, "qst": q, "asw": a,"sname": set_session(req), "users": get_users(), "topics": get_topics()})

#Ask
def ask(req):
	topics = Topic.objects.all()
	return render_to_response("ask.html", {"topics": topics,"sname": set_session(req) ,"users": get_users(), "topics": get_topics()}, context_instance = RequestContext(req))

def client(req):
	return render_to_response("client.html", {})

def addask(req):
	if req.method == "POST":
		if "title" in req.POST and "topic" in req.POST and "content" in req.POST:
			if "name" in req.session:
				title = req.POST["title"]
				topic_id = int(req.POST["topic"])
				content = req.POST["content"]
				try:
					u = User.objects.get(id=int(req.session["name"]))
					u.raiting = u.raiting + 1
					topic = Topic.objects.get(id = topic_id)
					u.save()
				except (Topic.DoesNotExist, User.DoesNotExist):
					return HttpResponse("Error")
				af = AskForm({"title" : title, "content" : content, "topic": topic_id})
				if af.is_valid():
					q = Question(title = title, topic = topic, content = content, user = u, date = datetime.datetime.now(), raiting = 0)
					q.save()
					return HttpResponseRedirect("../../qstadd/?qst_id={0}".format(q.id))
				else:
					return HttpResponse("Error Valid")
	return HttpResponse("")

#Notificatin Question Add
def qstadd(req):
	qst_id = 1
	if req.method == "GET":
		if "qst_id" in req.GET:
			qst_id = req.GET["qst_id"]
	return render_to_response("qstadd.html", {"sname": set_session(req), "users": get_users(), "topics": get_topics(), "qst_id": qst_id})

#Session:
def set_session(req):
	if "name" in req.session:
		sname = req.session["name"]
	else:
		sname = False
	return sname
	
def logout(req):
	if "name" in req.session:
		del req.session["name"]
	return HttpResponseRedirect("../1/")

#Ajax
def test_reg(req):	
	if req.method == "POST":
		name = req.POST['name'].strip()
		pwd = req.POST['password'].strip()
		email = req.POST['email'].strip()
		if name and pwd and email:
			rf = RegForm({'name': name, 'password': pwd, 'email': email})
			if rf.is_valid():
				if User.objects.filter(name = name).count() == 0:
					u = User(name = name, email = email, password = hashlib.sha1(pwd).hexdigest(), reg_date = datetime.datetime.now(), raiting = 0)
					u.save()
					req.session['name'] = u.id
					return HttpResponse('{"status": "ok"}')
				else:
					return HttpResponse('{"status": "error", "code": "1"}')
			else:
				return HttpResponse('{"status": "error", "code": "2"}') #Uncorrect data
	return HttpResponse('{"status": "error", "code": "3"}') # Other error

def like(req):
	if not "name" in req.session:
		return HttpResponse('{"status":"error","code":"5"}')
	if "type" in req.POST and "id" in req.POST and "sign" in req.POST:
		type = req.POST["type"]
		id = int(req.POST["id"])
		sign = req.POST["sign"]
		if type and id and sign:
			if type == "asw":
				try:
					a = Answer.objects.get(id = id)
					ua = a.user
					u = User.objects.get(id = req.session["name"])
					if AswLikes.objects.filter(asw = a, user = u).count() == 0:
						al = AswLikes(asw = a, user = u)
						if sign == "plus":
							a.raiting = a.raiting + 1
							ua.raiting = ua.raiting + 5
						elif sign == "minus":
							a.raiting = a.raiting - 1
							ua.raiting = ua.raiting - 2
						al.save()
						a.save()
						ua.save()
						return HttpResponse('{{"status":"ok","id":"{0}"}}'.format(id)) # Success
					else:
						return HttpResponse('{"status":"error","code":"1"}') #You have already rated
				except (Answer.DoesNotExist):
					return HttpResponse('{"status":"error","code":"2"}') #Answer Doesn't exist
			elif type == "qst":
				try:
					q = Question.objects.get(id = id)
					uq = q.user
					u = User.objects.get(id = req.session["name"])
					if QstLikes.objects.filter(qst = q, user = u).count() == 0:
						ql = QstLikes(qst = q, user = u)
						if sign == "plus":
							q.raiting = q.raiting + 1
							uq.raiting = uq.raiting + 3
						elif sign == "minus":
							q.raiting = q.raiting - 1
							uq.raiting = uq.raiting - 2
						ql.save()
						q.save()
						uq.save()
						return HttpResponse('{{"status":"ok","id":"{0}"}}'.format(id)) # Success
					else:
						return HttpResponse('{"status":"error","code":"1"}') #You have already rated
				except (Answer.DoesNotExist):
					return HttpResponse('{"status":"error","code":"3"}') #Question Doesn't exist
	return HttpResponse('{"status":"error","code":"4"}')

def answers(req):
	c = 30
	first_range = range(1, 6)
	if not "name" in req.session:
		 return HttpResponse('{"status":"error","code":"5"}'); #Only for registered users
	if "qst" in req.POST and "text" in req.POST:
		qst_id = req.POST['qst']
		text = req.POST['text']
		# handling a text
		if qst_id and text:
			try:
				q = Question.objects.get(id = qst_id)
				u = User.objects.get(id=req.session["name"])
				d = datetime.datetime.now()
				a = Answer(content = text, qst = q, user = u, date = "{0}-{1}-{2}".format(d.year, d.month, d.day)
									, flag = False, raiting = 0)
				a.save()
				lng = Answer.objects.filter(qst = qst_id).count()
				total = int(math.ceil(float(lng) / c)) # Number of pages (All pages)
				res = Answer.objects.filter(qst = qst_id)[(total - 1) * c : lng]
				s = ""
				for i in res:
					try:
						s = s + '{{"id":"{0}", "content":"{1}", "user":"{2}", "date":"{3}", "raiting":"{4}", "user_name":"{5}"}},'.format(i.id, i.content, i.user.id, i.date.strftime("%h %d, %Y"), i.raiting, i.user.name)
					except:
						s = s + '{{"id":"{0}", "content":"{1}", "user":"{2}", "date":"{3}", "raiting":"{4}", "user_name":"{5}"}},'.format(i.id, i.content, i.user.id, i.date, i.raiting, i.user.name)
				s = s[0:-1]
				
				show_first = True
				start = total - 3
				end = total 
				
				if total in first_range:
					show_first = False
					start = 1
				
				pag = '{{"show_first":"{0}", "start": "{1}", "end": "{2}"}}'.format(show_first, start, end);
				return HttpResponse('{{"status":"ok","asw":[{0}], "total":"{1}", "pag":{2}}}'.format(s, total, pag))
			except (Question.DoesNotExist, Answer.DoesNotExist, User.DoesNotExist):
				return HttpResponse('{"status":"error","code":"3"}') #Question or User Doesn't exist
	
	return HttpResponse('{"status":"error","code":"4"}')
	
def test(req):
	t = get_template("test.html")
	html = t.render(Context({"name": "Opa"}))
	return HttpResponse(html)
	
def get_user(req):
	if 'name' in req.POST and 'pas' in req.POST:
		name = req.POST["name"]
		p = req.POST['pas']
		if name and p:
			f = EnterForm({"name":name, "password":p})
			if f.is_valid():
				try:
					u = User.objects.get(name = name)
					if u.password == hashlib.sha1(p).hexdigest():
						req.session["name"] = u.id
						return HttpResponse('{"status":"ok"}')
					else:
						return HttpResponse('{"status":"error","error":"1"}') #Uncorrect Password
				except User.DoesNotExist:
					return HttpResponse('{"status":"error", "error":"2"}') #User does't exist
			else:
				return HttpResponse('{"status":"error", "error":"3"}')
	return HttpResponse('{"status":"error", "error":4}')


def topic(req, id):
	id = int(id)
	c = 20 # Visible columns on the page
	offset = 1 #  Number of the page
	
	if 'offset' in req.GET:
		offset = req.GET['offset']
		if offset:
			offset = int(offset)
	
	try:
		t = Topic.objects.get(id = id)
		q = t.question_set.all()[(offset - 1) * 20 : (c * offset - 1)]
	except (Topic.DoesNotExist, Question.DoesNotExist):
		return render_to_response("500.html", {"error":"topic"});
	
	lng = float(t.question_set.all().count())
	total = int(math.ceil(lng / c)) # Number of pages (All pages)
	first_range = range(1, 5)
	last_range = range((total - 3),  (total + 1))
	
			
	n = Topic.objects.all().count()
	if not id or id > n:
		id = 1
	
	has_prev = True
	has_next = True
	show_first = True
	show_last = True
	start = offset - 3
	end = offset + 3			
	
	if offset == 1:
		has_prev = False
		page_numbers = first_range
	
	if offset == total:
		has_next = False
		page_numbers = last_range
		
	if offset in first_range:
		show_first = False
		start = 1
	
	if offset in last_range:
		show_last = False
		end = total
	
 	paginator = {"has_prev": has_prev, "has_next": has_next, "current": offset, "show_first": show_first, "show_last": show_last, 
					"pages": total, "page_numbers": range(start, (end + 1)), "prev" : (offset - 1), "next": (offset + 1)}
	d = {"questions": q, "sname": set_session(req), "users": get_users(), "topics": get_topics()}
	return render_to_response("topic.html", dict(paginator.items() + d.items()))
