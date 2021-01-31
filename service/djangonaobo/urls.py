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
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import pay, sayhello, hello4, socket, checkstudentNET, studentcheckNET, editcheck, pluspointNET, subpointNET, randompickstudentNET
from myapp.views import naoindexNET, vocabularypreviewresultNET, beforeyoureadNET

urlpatterns = [

    path('admin/', admin.site.urls),
    path('add_pay/', pay),
    path('', include('gsheets.urls')),
    re_path(r'^$', sayhello),
    re_path(r'^hello4/', hello4),
    re_path(r'^socket/', socket),
    re_path(r'^studentcheck/', studentcheckNET),
    re_path(r'^checkstudent/', checkstudentNET),
    re_path(r'^edit/', editcheck),
    re_path(r'^pluspoint/', pluspointNET),
    re_path(r'^subpoint/', subpointNET),
    re_path(r'^randompickstudent/', randompickstudentNET),
    re_path(r'^naoindex/', naoindexNET),
    re_path(r'^vocabularypreviewresult/', vocabularypreviewresultNET),
    re_path(r'^beforeyoureadresult/', beforeyoureadNET)

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
