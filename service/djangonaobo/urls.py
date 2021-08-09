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
from myapp.views import pay, homepage, customizeclassinfopage, setnaoipNET, getnaoipNET, sayhello, home, checkstudentNET, studentcheckNET, editcheck, pluspointNET, subpointNET, randompickstudentNET
from myapp.views import naoindexNET, vocabularypreviewresultNET, beforeyoureadresultNET, vocabularyreviewresultNET, focusoncontentresultNET
from myapp.views import announcebeforeyoureadNET, getvocabularypreviewscoreNET, getvocabularyreviewscoreNET, getfocusoncontentscoreNET
from myapp.views import announcevocabularypreviewNET, announcefocusoncontentNET, announcevocabularyreviewNET
from myapp.views import changesectiontocriticalthinking, changesectiontostudentcheck, changesectiontobeforeyouread, changesectiontovocabularypreview, changesectiontofocusoncontent, changesectiontovocabularyreview
from myapp.views import checksection, vocabularypreviewdetail, focusoncontentdetail, vocabularyreviewdetail, readingNET, groupcheckok, getgroupstudents
from myapp.views import getvocabularypreviewanswerNET, getvocabularyreviewanswerNET
from myapp.views import getvocabularydetailNET, criticalthinkingrecord, announceuncheckedstudentNET, getstudentchecksituation, setclassstarttime, getnextstarttime, clock
from myapp.views import teachcustomizevocabulary, customizestudentslist, customizestudentchangepoint, customizestudentchangecheck, customizerandompickstudent, customizequiz
from myapp.views import zenbogetclassinfo, customizeclassinfosetting, startcustomizeautoclass, customizereading, customizeexercise, startautoclass, checkallgroupready, zenbogetready
from myapp.views import zenbochecksection, customizestudentcheck, readingpartsettingandgetting, customizediscussion, zenbogetdiscussion
urlpatterns = [

    path('admin/', admin.site.urls),
    path('add_pay/', pay),
    path('', include('gsheets.urls')),
    re_path(r'^$', sayhello),
    re_path(r'^homepage/', homepage),
    re_path(r'^home/', home),
    re_path(r'^studentcheck/', studentcheckNET),
    re_path(r'^getstudentchecksituation/', getstudentchecksituation),
    re_path(r'^checkstudent/', checkstudentNET),
    re_path(r'^edit/', editcheck),
    re_path(r'^pluspoint/', pluspointNET),
    re_path(r'^subpoint/', subpointNET),
    re_path(r'^randompickstudent/', randompickstudentNET),
    re_path(r'^naoindex/', naoindexNET),
    re_path(r'^reading/', readingNET),
    re_path(r'^customizeclassinfo/', customizeclassinfopage),
    re_path(r'^setnaoip/', setnaoipNET),
    re_path(r'^getnaoip/', getnaoipNET),
    re_path(r'^setstarttime/', setclassstarttime),
    re_path(r'^getnextstarttime/', getnextstarttime),
    re_path(r'^clock/', clock),

    re_path(r'^vocabularypreviewresult/', vocabularypreviewresultNET),
    re_path(r'^beforeyoureadresult/', beforeyoureadresultNET),
    re_path(r'^vocabularyreviewresult/', vocabularyreviewresultNET),
    re_path(r'^focusoncontentresult/', focusoncontentresultNET),

    re_path(r'^vocabularypreviewdetail/', vocabularypreviewdetail),
    re_path(r'^vocabularyreviewdetail/', vocabularyreviewdetail),
    re_path(r'^focusoncontentdetail/', focusoncontentdetail),

    re_path(r'^announcebeforeyouread/', announcebeforeyoureadNET),
    re_path(r'^announcevocabularypreview/', announcevocabularypreviewNET),
    re_path(r'^announcefocusoncontent/', announcefocusoncontentNET),
    re_path(r'^announcevocabularyreview/', announcevocabularyreviewNET),
    re_path(r'^announceuncheckedstudent/', announceuncheckedstudentNET),

    re_path(r'^getvocabularypreviewscore/', getvocabularypreviewscoreNET),
    re_path(r'^getvocabularyreviewscore/', getvocabularyreviewscoreNET),
    re_path(r'^getfocusoncontentscore/', getfocusoncontentscoreNET),
    re_path(r'^getvocabularypreviewscoredetail/', getvocabularypreviewanswerNET),
    re_path(r'^getvocabularyreviewscoredetail/', getvocabularyreviewanswerNET),
    # re_path(r'^getfocusoncontentscoredetail/', getfocusoncontentscoredetailNET),
    re_path(r'^getvocabularydetail/', getvocabularydetailNET),
    re_path(r'^criticalthinkingchoose/', criticalthinkingrecord),

    re_path(r'^changesectiontostudentcheck/', changesectiontostudentcheck),
    re_path(r'^changesectiontobeforeyouread/', changesectiontobeforeyouread),
    re_path(r'^changesectiontovocabualrypreview/', changesectiontovocabularypreview),
    re_path(r'^changesectiontofocusoncontent/', changesectiontofocusoncontent),
    re_path(r'^changesectiontovocabularyreview/', changesectiontovocabularyreview),
    re_path(r'^changesectiontocriticalthinking/', changesectiontocriticalthinking),
    re_path(r'^checksection/', checksection),
    re_path(r'^groupcheckok/', groupcheckok),
    re_path(r'^getgroupstudents/', getgroupstudents),

    # 更改後系統
    re_path(r'^teachcustomizevocabulary/', teachcustomizevocabulary),
    re_path(r'^customizestudentslist/', customizestudentslist),
    re_path(r'^changepoint/', customizestudentchangepoint),
    re_path(r'^changecheck/', customizestudentchangecheck),
    re_path(r'^pickonestudent/', customizerandompickstudent),
    re_path(r'^customizequiz/', customizequiz),
    re_path(r'^setclassinfo/', customizeclassinfosetting),
    re_path(r'^autoclasspage/', startcustomizeautoclass),
    re_path(r'^customizereading/', customizereading),
    re_path(r'^customizeexercise/', customizeexercise),
    re_path(r'^startautoclass/', startautoclass),
    re_path(r'^checkallgroupsready/', checkallgroupready),
    re_path(r'^zenbogetready/', zenbogetready),
    re_path(r'^getclassinfo/', zenbogetclassinfo),
    re_path(r'^zenbochecksection/', zenbochecksection),
    re_path(r'^zenbogetdiscussion/', zenbogetdiscussion),
    re_path(r'^customizestudentcheck/', customizestudentcheck),
    re_path(r'^readingpartsettingandgetting/', readingpartsettingandgetting),
    re_path(r'^customizediscussion/', customizediscussion)
]


admin.site.site_header = "Django Administration"
admin.site.index_title = "課程資料管理"