from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from librarymanagement.settings import EMAIL_HOST_USER
from django.db import IntegrityError


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})






def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                book = form.save()
                book.save()
                return render(request, 'library/bookadded.html')
            except IntegrityError:
                form.add_error('isbn', 'ISBN must be unique.')
    return render(request, 'library/addbook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'library/viewbook.html',{'books':books})

def guestview_view(request):
    books=models.Book.objects.all()
    return render(request,'library/guestview.html',{'books':books})

def studentview_view(request):
    books=models.Book.objects.all()
    return render(request,'library/guestview.html',{'books':books})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_book_view(request, book_id):
    book = get_object_or_404(models.Book, isbn=book_id)
    form = forms.BookForm(request.POST or None, request.FILES or None, instance=book)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                return render(request, 'library/bookadded.html')
            except IntegrityError:
                form.add_error('isbn', 'ISBN must be unique.')

    return render(request, 'library/update_book.html', {'form': form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_book_view(request, book_id):
    book = get_object_or_404(models.Book, isbn=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('view_book')

    return render(request, 'library/delete_book.html', {'book': book})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
    

        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'library/viewissuedbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

def aboutus_view(request):
    return render(request,'library/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['wapka1503@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form':sub})

def perform_search(query):
    # Perform the search query using the Book model
    results = models.Book.objects.filter(name__icontains=query)
    return results

def search_results(request):
    query = request.GET.get('query')  # Retrieve the search query from the GET parameters
    results = perform_search(query)  # Perform the search logic and get the search results
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'library/search_results.html', context)


def booking_view(request):
    return render(request, 'library/bookingbuku.html')


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from datetime import date, timedelta
from .models import Book, StudentExtra, BookLoan, Notification

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from datetime import date, timedelta
from .models import Book, StudentExtra, BookLoan

def borrow_book(request, book_id):
    book = get_object_or_404(Book, isbn=book_id)
    student = get_object_or_404(StudentExtra, user=request.user)

    if request.method == 'GET':
        # Check if there are existing loans for the book with status other than 'dikembalikan'
        existing_loan = BookLoan.objects.filter(book=book, student=student, status__in=['menunggu konfirmasi peminjaman', 'dipinjam']).first()

        if existing_loan:
            return render(request, 'library/popup.html')

        # Proceed with the borrowing process
        due_date = date.today() + timedelta(days=7)
        book_loan = BookLoan(student=student, book=book, date_due=due_date, status='menunggu konfirmasi peminjaman')
        book_loan.save()

        book.jumlah_buku -= 1
        book.save()

        return HttpResponseRedirect('/')

    return render(request, '/', {'book': book})

@login_required
def daftar_peminjaman(request):
    if request.method == 'POST':
        peminjaman_id = request.POST.get('peminjaman_id')
        peminjaman = get_object_or_404(BookLoan, id=peminjaman_id)
        peminjaman.status = 'Canceled'
        peminjaman.save()
        book = peminjaman.book
        book.jumlah_buku += 1
        book.save()
        return redirect('peminjaman_list')
    
    student_extra = StudentExtra.objects.get(user=request.user)
    peminjaman_list = BookLoan.objects.filter(student=student_extra).order_by('status')
    return render(request, 'library/pinjaman_list.html', {'peminjaman_list': peminjaman_list})

@login_required
def riwayat_peminjaman(request):
    student_extra = StudentExtra.objects.get(user=request.user)
    peminjaman_list = BookLoan.objects.filter(student=student_extra)
    return render(request, 'library/riwayat_peminjaman.html', {'peminjaman_list': peminjaman_list})

def view_peminjaman_admin(request):
    peminjaman_list2 = BookLoan.objects.all()
    return render(request, 'library/viewissuedbook.html', {'peminjaman_list2': peminjaman_list2})

def accept_peminjaman(request, peminjaman_id):
    peminjaman = get_object_or_404(BookLoan, id=peminjaman_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'dipinjam':
            peminjaman.status = 'dipinjam'
            peminjaman.save()
            return redirect('viewiss')
        elif status == 'ditolak':
            peminjaman.status = 'ditolak'
            peminjaman.save()
            book = peminjaman.book
            book.jumlah_buku += 1
            book.save()
            return redirect('viewiss')
    return render(request, 'library/viewissuedbook.html', {'peminjaman': peminjaman})

def view_pengembalian_admin(request):

    if request.method == 'POST':
        peminjaman_id = request.POST.get('peminjaman_id')
        peminjaman = get_object_or_404(BookLoan, id=peminjaman_id)
        peminjaman.status = 'dikembalikan'
        peminjaman.save()
        book = peminjaman.book
        book.jumlah_buku += 1
        book.save()
        return redirect('viewiss')
    
    peminjaman_list3 = BookLoan.objects.all()
    return render(request, 'library/pengembalian_admin.html', {'peminjaman_list3': peminjaman_list3})


# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect

# def custom_admin_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None and user.is_staff:
#             login(request, user)
#             return redirect('admin:index')
#         else:
#             error_message = 'Invalid username or password.'
#             return render(request, 'customadmin/login.html', {'error_message': error_message})
#     return render(request, 'customadmin/login.html')
