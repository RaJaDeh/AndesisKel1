from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['enrollment','branch']

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['name','isbn','author','category','jumlah_buku','lokasi_buku']
        
class IssuedBookForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    isbn2=forms.ModelChoiceField(queryset=models.Book.objects.all(),empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn')
    enrollment2=forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(),empty_label="Name and enrollment",to_field_name='enrollment',label='Name and enrollment')

class RequestForm(forms.ModelForm):
    isbn=forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Judul(ISBN)", to_field_name="isbn",
                                 label='Pilih Buku yang akan dipinjam ')
    nama = forms.CharField(label='Nama Peminjam', initial=models.RequestModel)
    issuedate = forms.DateField(label='Tanggal Peminjaman', initial=models.getnow)
    expirydate = forms.DateField(label='Tanggal Pengembalian', initial=models.get_expiry)
    
    class Meta :
        model = models.RequestModel
        fields = ['nama','issuedate','expirydate']
        
class PengembalianForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    enrollment2=forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(),
                                       empty_label="Cari",
                                       to_field_name='enrollment',
                                       label='Nama Peminjam')
    isbn2=forms.ModelChoiceField(queryset=models.Book.objects.all(),empty_label="Cari", 
                                 to_field_name="isbn",
                                 label='Judul Buku (ISBN)')
    pengembaliandate= forms.DateField(label='Tanggal Dikembalikan', initial=models.getnow)