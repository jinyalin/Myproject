'''
#use html templates
#test1
from django.http import HttpResponse
def index(req):
    return HttpResponse('<h1>hello welcome to Djiango</h1>')

#test2
from django.shortcuts import render_to_response
def index(req):
    return render_to_response('index.html',{})

#other method
from django.template import loader,Context
from django.http import HttpResponse
def index(req):
    t = loader.get_template('index.hmtl')
    c = Context({'uname':'alen'})
    html = t.render(c)
    return HttpResponse(html)
#othen method
from django.template import loader,Context,Template
from django.http import HttpResponse
def index(req):
    t = Template('<h1>hello {{uname}}</h1>')
    c = Context({'uname':'csvt'})
    return HttpResponse(t.render(c))
#test3
from django.shortcuts import render_to_response
def index(req):
    return render_to_response('index.html',{'title':'my page','user':'jinyalin'})

#test4
from django.shortcuts import render_to_response
def index(req):
    user = {'name':'jinyalin','age':'26','sex':'woman'}
    return render_to_response('index.html',{'title':'my page','user':user})

#test5
from django.shortcuts import render_to_response
class Person(object):
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
        
def index(req):
    user = Person('yzm',23,'male')
    return render_to_response('index.html',{'title':'my page','user':user})

#test6 zidiang>shuxing>fangfa>list
from django.shortcuts import render_to_response
class Person(object):
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
    def say(self):
        return "my name is :" + self.name
        
def index(req):
    user = Person('yzm',23,'male')
    book_list = ['python','java','php','web']
    user1 = {'name':'tom','age':23,'sex':'male'}
    return render_to_response('index.html',{'title':'my page','book_list':book_list,'usr':user1})

#database select operate  many to one
from django.shortcuts import render_to_response
from blog.models import Employee
def index(seq):
    emps = Employee.objects.all()
    return render_to_response('index.html',{'emps':emps})

#database select operate  many to many
from django.shortcuts import render_to_response
from blog.models import Author,Book

def show_author(req):
    authors = Author.objects.all()
    return render_to_response('show_author.html',{'authors':authors})

def show_book(req):
    books = Book.objects.all()
    return render_to_response('show_book.html',{'books':books})
'''
#form operate
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response

class UserForm(forms.Form):
    name = forms.CharField()
    
def register(req):
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponse('ok')
    else :
        form = UserForm()
    return render_to_response('register.html',{'form':form})

'''
#insert data
from blog.models import Employee
#method1
emp = Employee()
emp.name = 'Alen'
emp.save()
#method2
emp = Employee(name='Tom')
emp.save()
#method3
emp = Employee.objects.create(name='Max')

#select data
emps = Employee.objects.all()#those return object,to models.py add a method
eg:
class Employee(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name
'''