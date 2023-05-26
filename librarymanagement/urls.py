"""librarymanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView,LogoutView
from library.admin import admin_site
# from library.views import custom_admin_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),

    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),

    path('search/', views.search_results, name='search_results'),

    path('adminsignup', views.adminsignup_view),
    path('studentsignup', views.studentsignup_view),
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html')),
    

    path('logout', LogoutView.as_view(template_name='library/index.html')),
    path('afterlogin', views.afterlogin_view),

    path('books/<int:book_id>/', views.book_details, name='book_details'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),

    path('addbook', views.addbook_view),
    path('viewbook', views.viewbook_view, name='view_book'),
    path('guestview', views.guestview_view),
    path('studentview', views.studentview_view),
    path('issuebook', views.issuebook_view),
    path('viewissuedbook', views.view_peminjaman_admin, name="viewiss"),
    path('pengembalianadmin', views.view_pengembalian_admin, name="pengembalian"),
    path('viewstudent', views.viewstudent_view),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    path('update-book/<int:book_id>/', views.update_book_view, name='update_book'),
    path('delete-book/<int:book_id>/', views.delete_book_view, name='delete_book'),

    path('bookingbuku', views.booking_view),
    path('pinjaman_list', views.daftar_peminjaman, name='peminjaman_list'),
    path('riwayat_peminjaman', views.riwayat_peminjaman, name='riwayat_peminjaman'),
    path('customadmin/', admin_site.urls),

    path('accept-peminjaman/<int:peminjaman_id>/', views.accept_peminjaman, name='accept_peminjaman'),
    # path('customadmin/login/', custom_admin_login, name='custom_admin_login'),
]
