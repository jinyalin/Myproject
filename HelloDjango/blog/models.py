from django.db import models

#create tables and tables's desc
class Employee(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Blog(models.Model):
    name = models.CharField(max_length=30)
    entry = models.ForeignKey(Employee)
    
    def __str__(self):
        return self.name
sex_choices =(
              ('f','famale'),
              ('m','male'),
              )    
class User(models.Model):
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=1,choices=sex_choices)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=30)
    authors = models.ManyToManyField(Author)
    
    def __str__(self):
        return self.name

'''
many to one  (is) Blog to Employee
from blog.models import Employee,Blog
entry1 = Employee.objects.create(name='jinyalin')
entry2 = Employee.objects.create(name='xuwuqiang')
entry3 = Employee.objects.create(name='zhangxiaotian')
blog1 = Blog.objects.create(name='jyl',entry=entry1)
#many :
>>> blog1.entry
<Employee: jinyalin>
>>> blog1.entry_id
5
#one :
>>> entry1.blog_set.all()
[<Blog: jyl>]

---------------------------------------------
many to many (is) Author to Book
>>> from blog.models import Author,Book
>>> Author.objects.create(name='Alen')
<Author: Alen>
>>> Author.objects.create(name='Ben')
<Author: Ben>
>>> Author.objects.create(name='Carl')
<Author: Carl>
>>> Author.objects.create(name='Dev')
<Author: Dev>
>>> authors = Author.objects.all()
>>> authors
[<Author: Alen>, <Author: Ben>, <Author: Carl>, <Author: Dev>]
>>> b1 = Book()
>>> b1.name = 'python book1'
>>> b1.save()
>>> alen = Author.objects.get(name__exact='Alen')
>>> alen
<Author: Alen>
>>> b1.authors.add(alen)
>>> b1.authors.add(authors[1])
>>> b1.authors.all()
[<Author: Alen>, <Author: Ben>]
>>> b1.authors.add(authors[2])
>>> b1.authors.add(authors[3])
>>> b1.authors.all()
[<Author: Alen>, <Author: Ben>, <Author: Carl>, <Author: Dev>]
>>> b1.authors.remove(alen)
>>> b1.authors.all()
[<Author: Ben>, <Author: Carl>, <Author: Dev>]
>>> b1.authors.filter(name__exact='Carl')
[<Author: Carl>]

>>> alen.book_set.add(b1)
>>> alen.book_set.all()
[<Book: python book1>]
>>> alen.book_set.create(name='python book2')
<Book: python book2>
>>> alen.book_set.all()
[<Book: python book1>, <Book: python book2>]
>>> books = Book.objects.all()
>>> books
[<Book: python book1>, <Book: python book2>]
>>> alen.book_set.remove(books[0])
>>> alen.book_set.all()
[<Book: python book2>]

for author in Author.objects.all():
    for book in author.book_set.all():
        print book

'''