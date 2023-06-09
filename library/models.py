from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.core.exceptions import ValidationError
import cv2
from PIL import Image

class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Asal_Universitas = models.CharField(max_length=40)
    Asal_Daerah = models.CharField(max_length=40)

    def __str__(self):
        return self.user.first_name+'['+str(self.Asal_Universitas)+']'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice = [
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
    catchoice2 = [
        ('RAK A', 'RAK A'),
        ('RAK B', 'RAK B'),
        ('RAK C', 'RAK C'),
        ('RAK D', 'RAK D'),
        ('RAK E', 'RAK E')
    ]
    name = models.CharField(max_length=30)
    isbn = models.PositiveIntegerField(unique=True)
    author = models.CharField(max_length=40)
    category = models.CharField(max_length=30, choices=catchoice, default='education')
    jumlah_buku = models.PositiveIntegerField(default=0)
    lokasi_buku = models.CharField(max_length=30, choices=catchoice2, default='RAK A')
    cover = models.ImageField(upload_to='book_covers/', default='static/images/AdminIcon.jpg')

    def save(self, *args, **kwargs):
        # Memanggil metode save model yang asli
        super().save(*args, **kwargs)

        # Mengubah ukuran gambar setelah objek Book disimpan
        if self.cover:
            img = Image.open(self.cover.path)
            img = img.resize((150, 200))
            img.save(self.cover.path)
    
    def __str__(self):
        return str(self.name) + "[" + str(self.isbn) + "]"
    
    def clean(self):
        # Validasi unik ISBN
        existing_book = Book.objects.filter(isbn=self.isbn).exclude(pk=self.pk)
        if existing_book.exists():
            raise ValidationError('ISBN must be unique.')


def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssuedBook(models.Model):
    enrollment=models.CharField(max_length=30)
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return self.enrollment

class BookLoan(models.Model):
    STATUS_CHOICES = [
        ('menunggu konfirmasi peminjaman', 'Menunggu Konfirmasi Peminjaman'),
        ('dipinjam', 'Dipinjam'),
        ('menunggu konfirmasi pengembalian', 'Menunggu Konfirmasi Pengembalian'),
        ('dikembalikan', 'Dikembalikan'),
    ]
    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    date_due = models.DateField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def get_student(self):
        return self.student

    def __str__(self):
        return str(self.student) + " - " + str(self.book)
    

class Notification(models.Model):
    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.message

