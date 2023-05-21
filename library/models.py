from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta

class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi','Sci-Fi')
        ]
    catchoice2= [
        ('RAK A', 'RAK A'),
        ('RAK B', 'RAK B'),
        ('RAK C', 'RAK C'),
        ('RAK D', 'RAK D'),
        ('RAK E', 'RAK E')
        ]
    name=models.CharField(max_length=30)
    isbn=models.PositiveIntegerField()
    author=models.CharField(max_length=40)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    jumlah_buku=models.PositiveIntegerField(default=0)
    lokasi_buku = models.CharField(max_length=30,choices=catchoice2,default='RAK A')
    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)

def getnow():
    return datetime.today()

class IssuedBook(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    enrollment=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return self.enrollment

class Pengembalian(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    enrollment=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    pengembaliandate=models.DateField(default=getnow)
    def __str__(self):
        return self.enrollment
    
class RequestModel(models.Model):
    namapeminjam = models.CharField(max_length=30)
    isbn = models.CharField(max_length=30)
    issuedate = models.DateField(default=getnow)
    expirydate = models.DateField(default=get_expiry)
    
    def __str__(self):
        return self.namapeminjam
    
    def save(self, *args, **kwargs):
        if not self.namapeminjam:  # Hanya mengisi jika belum terisi
            student = StudentExtra.objects.get(user=self.user)
            self.namapeminjam = student.get_name()
        super().save(*args, **kwargs)

