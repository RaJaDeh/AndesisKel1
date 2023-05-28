from django.contrib import admin
from .models import Book,StudentExtra,IssuedBook,BookLoan
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)


class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)


class IssuedBookAdmin(admin.ModelAdmin):
    pass
admin.site.register(IssuedBook, IssuedBookAdmin)

class BookLoanAdmin(admin.ModelAdmin):
    list_display = ['student', 'book', 'date_issued', 'date_due', 'status']
    list_filter = ['status']
    search_fields = ['student__user__username', 'book__name']

admin.site.register(BookLoan, BookLoanAdmin)

from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'message')

admin.site.register(Notification, NotificationAdmin)

from django.contrib.admin import AdminSite
class CustomAdminSite(AdminSite):
    site_header = 'Admin Panel'
    site_title = 'Admin Panel'
    index_title = 'Welcome to the Admin Panel'

admin_site = CustomAdminSite(name='customadmin')

from django.contrib.admin import AdminSite
from django.shortcuts import render, redirect
class LibraryAdminSite(AdminSite):
    site_header = 'Library Admin'
    site_title = 'Library Admin'
    index_title = 'Welcome to the Library Admin'
    def login(self, request, extra_context=None):
        return redirect('custom_admin_login')

library_admin_site = LibraryAdminSite(name='libraryadmin')



