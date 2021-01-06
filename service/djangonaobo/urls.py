"""djangonaobo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from myapp.views import pay, sayhello, hello3, hello4, socket, uncheckedstudentNET, studentcheckNET

urlpatterns = [

    path('admin/', admin.site.urls),
    path('add_pay/', pay),
    #re_path(r'^teachercheckstudent/',teachercheckstudent),
    re_path(r'^$', sayhello),
    re_path(r'^hello3/(\w+)/$', hello3),
    re_path(r'^hello4/', hello4),
    re_path(r'^socket/', socket),
    re_path(r'^studentcheck/', studentcheckNET),
    re_path(r'^uncheckedstudent/', uncheckedstudentNET)
]
