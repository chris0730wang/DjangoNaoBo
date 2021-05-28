from django.shortcuts import render, redirect
from .models import Pay, studentcheck, VocabularyPreview, U10R1VocabularyPreviewAns, U10R2VocabularyPreviewAns
from .models import BeforeYouRead, U10BeforeYouReadAns, FocusOnContent, U10R1FocusonContentAns, U10R2FocusonContentAns
from .models import VocabularyReview, U10R1VocabularyReviewAns, U10R2VocabularyReviewAns, VocabularyDetail, SetNaoIP, SetStartTime
from .models import CustomizeStudentList, CustomizeVocabulary
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db.models import Q
from django.core import serializers

section = ["section", "section", "section", "section", "section"]
vocabularylist = []


def pay(request):

    if request.method == 'POST':
        item_spend = request.POST.get('item_spend')
        id = request.POST.get('id')
        money = request.POST.get('money')
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')
        isPri = request.POST.get('isPri')
        fun = request.POST.get('fun')
        if fun == '1':
            Pay.objects.create(id=id, item_spend=item_spend, money=money, year=year, month=month, day=day, isPri=isPri)
            try:
                t = Pay.objects.get(id=id)
                return HttpResponse("add_ok")
            except ObjectDoesNotExist:
                return HttpResponse("add_error")
        elif fun == '2':
            try:
                temp = Pay.objects.get(id=id)
                temp.delete()
                return HttpResponse("delete_ok")
            except ObjectDoesNotExist:
                return HttpResponse("not_found")
    else:
        return HttpResponse("error")

# 全部網頁的連結
def homepage(request):
    return render(request, "homepage.html", locals())

# 設定Nao IP的網頁
def CustomizeClassInfo(request):
    return render(request, "CustomizeClassInfo.html", locals())

# 設定Nao IP的url
def setnaoipNET(request):
    naoip = request.GET.get('ip')
    SetNaoIP.objects.create(IPAddress=naoip)
    print(naoip+"已儲存")
    return JsonResponse({'result': 'Save Successfully'})

# 設定系統開始時間
def setclassstarttime(request):
    starttime = request.GET.get('starttime')
    print(parse_datetime(starttime))
    SetStartTime.objects.create(starttime=starttime)
    return JsonResponse({'result': 'Save Successfully'})

# 網頁抓取資料庫中最新的Nao IP來連線
def getnaoipNET(request):
    newestrecord = SetNaoIP.objects.all().last()
    print(newestrecord.IPAddress)
    return JsonResponse({'IP': newestrecord.IPAddress})

# 網頁抓取資料庫中最新設定的課程時間
def getnextstarttime(request):
    newestrecord = SetStartTime.objects.all().last()
    print(newestrecord.starttime)
    if timezone.now() < newestrecord.starttime:
        timecomparison = "notyet"
    elif (timezone.now() - newestrecord.starttime).total_seconds() > 3600:
        timecomparison = "Expired"
    else:
        timecomparison = "OK"
    return JsonResponse({'starttime': str(newestrecord.starttime), 'timecomparison': timecomparison})

# Just Say Hello
def sayhello(request):

    return HttpResponse("Hello django !")

# Say Hello too
def hello2(request,username):

    return HttpResponse("Hello " + username)

# 之前測試用，無用處
def naoindexNET(request):
    return render(request, "naoindex.html", locals())

# 計時時鐘
def clock(request):
    sec = request.GET.get('sec')
    return render(request, "clock.html", locals())

# 首頁
@csrf_exempt
def home(request):
    nextstarttime = SetStartTime.objects.all().last()
    if timezone.now() < nextstarttime.starttime:
        result = "尚未到達預定上課時間，您可重新設定上課時間或等待。"
    elif (timezone.now() - nextstarttime.starttime).total_seconds() > 3600:
        result = "已超過預定時間一小時，請重新設定！"
    else:
        result = "已可開始課程，點選開始課程按鈕後將進入點名階段。"
    return render(request, "home.html", locals())

# 學生名單列表 首頁中的Students部分
def checkstudentNET(request):

    checkedstudent1 = studentcheck.objects.filter(cGroup='1').order_by('id')
    checkedstudent2 = studentcheck.objects.filter(cGroup='2').order_by('id')
    checkedstudent3 = studentcheck.objects.filter(cGroup='3').order_by('id')
    checkedstudent4 = studentcheck.objects.filter(cGroup='4').order_by('id')
    checkedstudent5 = studentcheck.objects.filter(cGroup='5').order_by('id')
    checkedstudent6 = studentcheck.objects.filter(cGroup='6').order_by('id')

    errormessage = " (讀取錯誤 !)"
    return render(request, "uncheckedstudent.html", locals())

# 為了查看學生每週的簽到情形
def getstudentchecksituation(request):

    idlist = ['', '', '', '', '', '']
    checksituationlist = ['', '', '', '', '', '']
    group = request.GET.get('group')
    week = request.GET.get('week')
    index = 0
    groupstudent = studentcheck.objects.filter(cGroup=group).order_by('id')
    for student in groupstudent:
        idlist[index] = student.cId
        if week == '1':
            checksituationlist[index] = student.FirstweekCheck
        elif week == '2':
            checksituationlist[index] = student.SecondweekCheck
        elif week == '3':
            checksituationlist[index] = student.ThirdweekCheck
        elif week == '4':
            checksituationlist[index] = student.ForthweekCheck
        else:
            print("Error")
        index += 1
    print(idlist)
    print(checksituationlist)
    return JsonResponse({'cId1': idlist[0], 'cId2': idlist[1], 'cId3': idlist[2], 'cId4': idlist[3], 'cId5': idlist[4], 'cId6': idlist[5],
                         'check1': checksituationlist[0], 'check2': checksituationlist[1], 'check3': checksituationlist[2], 'check4': checksituationlist[3], 'check5': checksituationlist[4], 'check6': checksituationlist[5]})

# 更改學生的簽到狀況
def editcheck(request):

    cId = request.GET.get('cId')
    week = request.GET.get('week')
    print("學號", cId, "進行更動 ！")

    t = studentcheck.objects.get(cId=cId)
    try:
        if week == '1':
            if t.FirstweekCheck == '已簽到':
                t.FirstweekCheck = '尚未簽到'
                t.save()
                print("成功")
            elif t.FirstweekCheck == '尚未簽到':
                t.FirstweekCheck = '已簽到'
                t.save()
                print("成功")
        elif week == '2':
            if t.SecondweekCheck == '已簽到':
                t.SecondweekCheck = '尚未簽到'
                t.save()
                print("成功")
            elif t.SecondweekCheck == '尚未簽到':
                t.SecondweekCheck = '已簽到'
                t.save()
                print("成功")
        elif week == '3':
            if t.ThirdweekCheck == '已簽到':
                t.ThirdweekCheck = '尚未簽到'
                t.save()
                print("成功")
            elif t.ThirdweekCheck == '尚未簽到':
                t.ThirdweekCheck = '已簽到'
                t.save()
                print("成功")
        elif week == '4':
            if t.ForthweekCheck == '已簽到':
                t.ForthweekCheck = '尚未簽到'
                t.save()
                print("成功")
            elif t.ForthweekCheck == '尚未簽到':
                t.ForthweekCheck = '已簽到'
                t.save()
                print("成功")
        return JsonResponse({"responsemessage": "更改成功"})
    except:
        return JsonResponse({"responsemessage": "更改失敗"})

# 學生藉由Zenbo Junior呼叫此views進行簽到
def studentcheckNET(request):

    groupzenbo = request.GET.get('zenbo')
    cId = request.GET.get('cId')
    print("學號", cId)
    week = request.GET.get('week')
    print("第", week, "週")
    t = studentcheck.objects.get(cId=cId)
    if int(groupzenbo) == t.cGroup:
        if week == '1':
            t.FirstweekCheck = "已簽到"
        if week == '2':
            t.SecondweekCheck = '已簽到'
        if week == '3':
            t.ThirdweekCheck = '已簽到'
        if week == '4':
            t.ForthweekCheck = '已簽到'
        t.save()
        print("簽到成功")
        return JsonResponse({'cId': t.cId, 'cName': t.cName, 'cGroup': t.cGroup})
    else:
        return JsonResponse({'cId': t.cId, 'cName': t.cName, 'cGroup': t.cGroup})

# 老師進行加分
def pluspointNET(request):

    cId = request.GET.get('cId')
    print("學號", cId, "進行加分")
    try:
        t = studentcheck.objects.get(cId=cId)
        t.point += 1
        t.save()
        print("成功")
        return JsonResponse({"responsemessage": "加分成功"})
    except:
        return JsonResponse({"responsemessage": "加分失敗"})

# 老師進行扣分
def subpointNET(request):

    cId = request.GET.get('cId')
    print("學號", cId, "進行扣分")
    try:
        t = studentcheck.objects.get(cId=cId)
        t.point -= 1
        t.save()
        print("成功")
        return JsonResponse({"responsemessage": "扣分成功"})
    except:
        return JsonResponse({"responsemessage": "扣分失敗"})

# 隨機抽取學生
def randompickstudentNET(request):

    group = request.GET.get('group')
    week = request.GET.get('week')
    print(group+"  "+week)
    num = 0
    if week == '1':
        while True:
            students = studentcheck.objects.filter(cGroup=group, FirstweekCheck="已簽到", picked=num).order_by(
                '?')
            if students.count() > 0:
                print("a")
                t = students.first()
                break
            else:
                print("c")
                num += 1
            # elif not students.exists():
            #     print("b")
            #     return JsonResponse({'result': 'Error ! 名單中無已簽到學生'})
    elif week == '2':
        while True:
            if group == 'all':
                students = studentcheck.objects.filter(SecondweekCheck="已簽到", picked=num).order_by('?')
            else:
                students = studentcheck.objects.filter(cGroup=group, SecondweekCheck="已簽到", picked=num).order_by(
                    '?')
            if students.count() > 0:
                t = students.first()
                break
            elif not students.exists():
                return JsonResponse({'picked': 'Error ! 名單中無已簽到學生'})
            else:
                num += 1
    elif week == '3':
        while True:
            students = studentcheck.objects.filter(cGroup=group, ThirdweekCheck="已簽到", picked=num).order_by(
                    '?')
            if students.count() > 0:
                t = students.first()
                break
            elif not students.exists():
                return JsonResponse({'picked': 'Error ! 名單中無已簽到學生'})
            else:
                num += 1
    elif week == '4':
            while True:
                students = studentcheck.objects.filter(cGroup=group, ForthweekCheck="已簽到", picked=num).order_by(
                    '?')
                if students.count() > 0:
                    t = students.first()
                    break
                elif not students.exists():
                    return JsonResponse({'picked': 'Error ! 名單中無已簽到學生'})
                else:
                    num += 1
    t.picked += 1
    t.save()
    print("抽點學生為：" + t.cName)
    return JsonResponse({'result': t.cName})

# reading 網頁
def readingNET(request):

    return render(request,"readaloud.html",locals())

# before you read 學生作答記錄
def beforeyoureadresultNET(request):

    try:
        unit = request.GET.get('unit')
        print("unit", unit)
        if unit == '10':
            for i in range(1, 5):
                if i == 1:
                    question = BeforeYouRead.objects.get(unit=unit, number=1)
                    studentans = U10BeforeYouReadAns.objects.filter(q1answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q1answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q1answer=question.option3)
                    question.numof3 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q1answer=question.option4)
                    question.numof4 = studentans.count()
                    question.save()
                elif i == 2:
                    question = BeforeYouRead.objects.get(unit=unit, number=2)
                    studentans = U10BeforeYouReadAns.objects.filter(q2answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q2answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q2answer=question.option3)
                    question.numof3 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q2answer=question.option4)
                    question.numof4 = studentans.count()
                    question.save()
                elif i == 3:
                    question = BeforeYouRead.objects.get(unit=unit, number=3)
                    studentans = U10BeforeYouReadAns.objects.all()
                    if studentans.count() != 0:
                        question.numof1 = 0
                        question.numof2 = 0
                        question.numof3 = 0
                        question.numof4 = 0
                        question.numof5 = 0
                        question.save()
                        question = BeforeYouRead.objects.get(unit=unit, number=3)
                        for j in range(0, studentans.count()):
                            studentansset = U10BeforeYouReadAns.objects.all()[j]
                            if question.option1 in studentansset.q3answer:
                                question.numof1 = question.numof1 + 1
                            if question.option2 in studentansset.q3answer:
                                question.numof2 = question.numof2 + 1
                            if question.option3 in studentansset.q3answer:
                                question.numof3 = question.numof3 + 1
                            if question.option4 in studentansset.q3answer:
                                question.numof4 = question.numof4 + 1
                            if question.option5 in studentansset.q3answer:
                                question.numof5 = question.numof5 + 1
                    question.save()
                elif i == 4:
                    question = BeforeYouRead.objects.get(unit=unit, number=4)
                    studentans = U10BeforeYouReadAns.objects.filter(q4answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q4answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q4answer=question.option3)
                    question.numof3 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q3answer=question.option4)
                    question.numof4 = studentans.count()
                    question.save()
        questionset = BeforeYouRead.objects.filter(unit=unit).order_by('number')

    except:
        print("error")
    return render(request, "beforeyoureadresult.html", locals())

# vocabulary preview 學生作答記錄
def vocabularypreviewresultNET(request):

    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        print("Unit", unit, "Reading", reading)
        correctansset = VocabularyPreview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        if unit == '10' and reading == '1':
            studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
            numofansstudent = studentans.count()
            for i in range(1, 9):
                correctans = VocabularyPreview.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 3:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 4:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 5:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 6:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 7:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 8:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                correctans.save()
        elif unit == '10' and reading == '2':
            studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
            numofansstudent = studentans.count()
            for i in range(1, 9):
                correctans = VocabularyPreview.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 3:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 4:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 5:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 6:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 7:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 8:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                correctans.save()
    except:
        print("error ! ")
        errormessage = "Error !"
    return render(request, "vocabularypreviewresult.html", locals())

# focus on content 學生作答記錄
def focusoncontentresultNET(request):

    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        print("Unit", unit, "Reading", reading)
        correctansset = FocusOnContent.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        if unit == '10' and reading == '1':
            studentansset = U10R1FocusonContentAns.objects.all().order_by('cId')
            numofansstudent = studentansset.count()
            for i in range(1, 8):
                correctans = FocusOnContent.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 3:
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 4:
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 5:
                    studentans = U10R1FocusonContentAns.objects.filter(q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 6:
                    studentans = U10R1FocusonContentAns.objects.filter(q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 7:
                    studentans = U10R1FocusonContentAns.objects.filter(q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                correctans.save()
        if unit == '10' and reading == '2':
            studentansset = U10R2FocusonContentAns.objects.all().order_by('cId')
            numofansstudent = studentansset.count()
            for i in range(1, 11):
                correctans = FocusOnContent.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 3:
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 4:
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 5:
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 6:
                    studentans = U10R2FocusonContentAns.objects.filter(q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 7:
                    studentans = U10R2FocusonContentAns.objects.filter(q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 8:
                    studentans = U10R2FocusonContentAns.objects.filter(q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 9:
                    studentans = U10R2FocusonContentAns.objects.filter(q9answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q9answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q9answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 10:
                    studentans = U10R2FocusonContentAns.objects.filter(q10answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q10answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q10answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                correctans.save()
    except:
        print("error !")
    return render(request, "focusoncontentresult.html", locals())

# vocabulary review 學生作答記錄
def vocabularyreviewresultNET(request):

    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        print("Unit", unit, "Reading", reading)
        correctansset = VocabularyReview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        if unit == '10' and reading == '1':
            studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
            numofansstudent = studentans.count()
            for i in range(1, 9):
                correctans = VocabularyReview.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 3:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 4:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 5:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 6:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 7:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 8:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                correctans.save()
        elif unit == '10' and reading == '2':
            studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
            numofansstudent = studentans.count()
            for i in range(1, 9):
                correctans = VocabularyReview.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 3:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 4:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 5:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 6:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 7:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 8:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                correctans.save()
    except:
        print("error ! ")
        errormessage = "Error !"
    return render(request, "vocabularyreviewresult.html", locals())

# 各組學生vocabulary preview的分數
def vocabularypreviewdetail(request):

    def countavg(group, reading):
        total = 0
        count = 0
        if reading == 1:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('vp1point')
            for student in groupcount:
                if student.vp1point is not None:
                    total += student.vp1point
                    count += 1
        elif reading == 2:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('vp2point')
            for student in groupcount:
                if student.vp2point is not None:
                    total += student.vp2point
                    count += 1
        if count == 0:
            count = 1
        avg = total / count
        return avg

    def savepoint(group, reading):
        studentgroup = studentcheck.objects.filter(cGroup=group).order_by('cId')
        if reading == 1:
            for student in studentgroup:
                t = U10R1VocabularyPreviewAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.vp1point = t.first().point
                    student.save()
        elif reading == 2:
            for student in studentgroup:
                t = U10R2VocabularyPreviewAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.vp2point = t.first().point
                    student.save()
        return studentgroup

    unit = request.GET.get('unit')
    reading = request.GET.get('reading')

    if unit == '10' and reading == '1':
        group1 = savepoint(1, 1)
        group2 = savepoint(2, 1)
        group3 = savepoint(3, 1)
        group4 = savepoint(4, 1)
        group5 = savepoint(5, 1)
        group1avg = countavg(1, 1)
        group2avg = countavg(2, 1)
        group3avg = countavg(3, 1)
        group4avg = countavg(4, 1)
        group5avg = countavg(5, 1)
        return render(request, "vocabularypreviewdetail.html", locals())

    elif unit == '10' and reading == '2':
        group1 = savepoint(1, 2)
        group2 = savepoint(2, 2)
        group3 = savepoint(3, 2)
        group4 = savepoint(4, 2)
        group5 = savepoint(5, 2)
        group1avg = countavg(1, 2)
        group2avg = countavg(2, 2)
        group3avg = countavg(3, 2)
        group4avg = countavg(4, 2)
        group5avg = countavg(5, 2)
        return render(request, "vocabularypreviewdetail2.html", locals())

# 各組學生focus on content的分數
def focusoncontentdetail(request):

    def countavg(group, reading):
        total = 0
        count = 0
        if reading == 1:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('foc1point')
            for student in groupcount:
                if student.foc1point is not None:
                    total += student.foc1point
                    count += 1
        elif reading == 2:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('foc2point')
            for student in groupcount:
                if student.foc2point is not None:
                    total += student.foc2point
                    count += 1

        if count == 0:
            count = 1
        avg = total / count
        return avg

    def savepoint(group, reading):
        studentgroup = studentcheck.objects.filter(cGroup=group).order_by('cId')
        if reading == 1:
            for student in studentgroup:
                t = U10R1FocusonContentAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.foc1point = t.first().point
                    student.save()
        elif reading == 2:
            for student in studentgroup:
                t = U10R2FocusonContentAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.foc2point = t.first().point
                    student.save()
        return studentgroup

    unit = request.GET.get('unit')
    reading = request.GET.get('reading')

    if unit == '10' and reading == '1':
        group1 = savepoint(1, 1)
        group2 = savepoint(2, 1)
        group3 = savepoint(3, 1)
        group4 = savepoint(4, 1)
        group5 = savepoint(5, 1)
        group1avg = countavg(1, 1)
        group2avg = countavg(2, 1)
        group3avg = countavg(3, 1)
        group4avg = countavg(4, 1)
        group5avg = countavg(5, 1)
        return render(request, "focusoncontentdetail.html", locals())

    elif unit == '10' and reading == '2':
        group1 = savepoint(1, 2)
        group2 = savepoint(2, 2)
        group3 = savepoint(3, 2)
        group4 = savepoint(4, 2)
        group5 = savepoint(5, 2)
        group1avg = countavg(1, 2)
        group2avg = countavg(2, 2)
        group3avg = countavg(3, 2)
        group4avg = countavg(4, 2)
        group5avg = countavg(5, 2)
        return render(request, "focusoncontentdetail2.html", locals())

# 各組學生vocabulary review的分數
def vocabularyreviewdetail(request):


    def countavg(group, reading):
        total = 0
        count = 0
        if reading == 1:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('vr1point')
            for student in groupcount:
                if student.vr1point is not None:
                    total += student.vr1point
                    count += 1
        elif reading == 2:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('vr2point')
            for student in groupcount:
                if student.vr2point is not None:
                    total += student.vr2point
                    count += 1

        if count == 0:
            count = 1
        avg = total / count
        return avg

    def savepoint(group, reading):
        studentgroup = studentcheck.objects.filter(cGroup=group).order_by('cId')
        if reading == 1:
            for student in studentgroup:
                t = U10R1VocabularyReviewAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.vr1point = t.first().point
                    student.save()
        elif reading == 2:
            for student in studentgroup:
                t = U10R2VocabularyReviewAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.vr2point = t.first().point
                    student.save()
        return studentgroup

    unit = request.GET.get('unit')
    reading = request.GET.get('reading')

    if unit == '10' and reading == '1':
        group1 = savepoint(1, 1)
        group2 = savepoint(2, 1)
        group3 = savepoint(3, 1)
        group4 = savepoint(4, 1)
        group5 = savepoint(5, 1)
        group1avg = countavg(1, 1)
        group2avg = countavg(2, 1)
        group3avg = countavg(3, 1)
        group4avg = countavg(4, 1)
        group5avg = countavg(5, 1)
        return render(request, "vocabularyreviewdetail.html", locals())

    elif unit == '10' and reading == '2':
        group1 = savepoint(1, 2)
        group2 = savepoint(2, 2)
        group3 = savepoint(3, 2)
        group4 = savepoint(4, 2)
        group5 = savepoint(5, 2)
        group1avg = countavg(1, 2)
        group2avg = countavg(2, 2)
        group3avg = countavg(3, 2)
        group4avg = countavg(4, 2)
        group5avg = countavg(5, 2)
        return render(request, "vocabularyreviewdetail2.html", locals())

# 將before you read學生們得作答記錄轉成語句回傳給Nao公布
def announcebeforeyoureadNET(request):

    QNumber = []
    QQuestion = []
    Qoption1 = []
    Qoption2 = []
    Qoption3 = []
    Qoption4 = []
    Qoption5 = []
    Qnumof1 = []
    Qnumof2 = []
    Qnumof3 = []
    Qnumof4 = []
    Qnumof5 = []
    try:
        unit = request.GET.get('unit')
        beforeyoureadset = BeforeYouRead.objects.filter(unit=unit).order_by('number')
        for beforeyouread in beforeyoureadset:
            QNumber.append(beforeyouread.number)
            QQuestion.append(beforeyouread.question)
            Qoption1.append(beforeyouread.option1)
            Qoption2.append(beforeyouread.option2)
            Qoption3.append(beforeyouread.option3)
            Qoption4.append(beforeyouread.option4)
            Qoption5.append(beforeyouread.option5)
            Qnumof1.append(beforeyouread.numof1)
            Qnumof2.append(beforeyouread.numof2)
            Qnumof3.append(beforeyouread.numof3)
            Qnumof4.append(beforeyouread.numof4)
            Qnumof5.append(beforeyouread.numof5)
    except:
        print("error !")
    return JsonResponse({'QNumber': QNumber, 'QQuestion': QQuestion, 'Qoption1': Qoption1, 'Qoption2': Qoption2,
                        'Qoption3': Qoption3, 'Qoption4': Qoption4, 'Qoption5': Qoption5, 'Qnumof1': Qnumof1,
                        'Qnumof2': Qnumof2, 'Qnumof3': Qnumof3, 'Qnumof4': Qnumof4, 'Qnumof5': Qnumof5})

# 將vocabulary preview學生們得作答記錄轉成語句回傳給Nao公布
def announcevocabularypreviewNET(request):

    QNumber = []
    QQuestion = []
    Qoption1 = []
    Qoption2 = []
    Qoption3 = []
    Qnumof1 = []
    Qnumof2 = []
    Qnumof3 = []
    Qcorrectans = []
    Qfalsepercent = []
    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        vocabularypreviewset = VocabularyPreview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        for vocabularypreview in vocabularypreviewset:
            QNumber.append(vocabularypreview.questionnum)
            QQuestion.append(vocabularypreview.question)
            Qoption1.append(vocabularypreview.option1)
            Qoption2.append(vocabularypreview.option2)
            Qoption3.append(vocabularypreview.option3)
            Qnumof1.append(vocabularypreview.numof1)
            Qnumof2.append(vocabularypreview.numof2)
            Qnumof3.append(vocabularypreview.numof3)
            Qcorrectans.append(vocabularypreview.correctans)
            Qfalsepercent.append(vocabularypreview.falsepercent)
    except:
        print("error !")
    return JsonResponse({'QNumber': QNumber, 'QQuestion': QQuestion, 'Qoption1': Qoption1, 'Qoption2': Qoption2,
                        'Qoption3': Qoption3, 'Qnumof1': Qnumof1, 'Qnumof2': Qnumof2, 'Qnumof3': Qnumof3, 'Qcorrectans': Qcorrectans,
                         'Qfalsepercent': Qfalsepercent})

# 將focus on content學生們得作答記錄轉成語句回傳給Nao公布
def announcefocusoncontentNET(request):

    QNumber = []
    QQuestion = []
    Qoption1 = []
    Qoption2 = []
    Qoption3 = []
    Qoption4 = []
    Qoption5 = []
    Qnumof1 = []
    Qnumof2 = []
    Qnumof3 = []
    Qnumof4 = []
    Qnumof5 = []
    Qcorrectans = []
    Qfalsepercent = []
    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        focusoncontentset = FocusOnContent.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        for focusoncontent in focusoncontentset:
            QNumber.append(focusoncontent.questionnum)
            QQuestion.append(focusoncontent.question)
            Qoption1.append(focusoncontent.option1)
            Qoption2.append(focusoncontent.option2)
            Qoption3.append(focusoncontent.option3)
            Qoption4.append(focusoncontent.option4)
            Qoption5.append(focusoncontent.option5)
            Qnumof1.append(focusoncontent.numof1)
            Qnumof2.append(focusoncontent.numof2)
            Qnumof3.append(focusoncontent.numof3)
            Qnumof4.append(focusoncontent.numof4)
            Qnumof5.append(focusoncontent.numof5)
            Qcorrectans.append(focusoncontent.correctans)
            Qfalsepercent.append(focusoncontent.falsepercent)
    except:
        print("errorr !")
    return JsonResponse({'QNumber': QNumber, 'QQuestion': QQuestion, 'Qoption1': Qoption1, 'Qoption2': Qoption2,
                        'Qoption3': Qoption3, 'Qoption4': Qoption4, 'Qoption5': Qoption5, 'Qnumof1': Qnumof1,
                         'Qnumof2': Qnumof2, 'Qnumof3': Qnumof3, 'Qnumof4': Qnumof4, 'Qnumof5': Qnumof5,
                         'Qcorrectans': Qcorrectans, 'Qfalsepercent': Qfalsepercent})

# 將vocabulary review學生們得作答記錄轉成語句回傳給Nao公布
def announcevocabularyreviewNET(request):

    QNumber = []
    QQuestion = []
    Qoption1 = []
    Qoption2 = []
    Qoption3 = []
    Qnumof1 = []
    Qnumof2 = []
    Qnumof3 = []
    Qcorrectans = []
    Qfalsepercent = []
    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        vocabularyreviewset = VocabularyReview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        for vocabularyreview in vocabularyreviewset:
            QNumber.append(vocabularyreview.questionnum)
            QQuestion.append(vocabularyreview.question)
            Qoption1.append(vocabularyreview.option1)
            Qoption2.append(vocabularyreview.option2)
            Qoption3.append(vocabularyreview.option3)
            Qnumof1.append(vocabularyreview.numof1)
            Qnumof2.append(vocabularyreview.numof2)
            Qnumof3.append(vocabularyreview.numof3)
            Qcorrectans.append(vocabularyreview.correctans)
            Qfalsepercent.append(vocabularyreview.falsepercent)
    except:
        print("error !")
    return JsonResponse({'QNumber': QNumber, 'QQuestion': QQuestion, 'Qoption1': Qoption1, 'Qoption2': Qoption2,
                        'Qoption3': Qoption3, 'Qnumof1': Qnumof1, 'Qnumof2': Qnumof2, 'Qnumof3': Qnumof3, 'Qcorrectans': Qcorrectans,
                         'Qfalsepercent': Qfalsepercent})

# 唱名未簽到的學生
def announceuncheckedstudentNET(request):

    week = request.GET.get('week')
    uncheckedstudentname = []
    if week == '1':
        uncheckedstudent = studentcheck.objects.filter(FirstweekCheck="尚未簽到")
    elif week == '2':
        uncheckedstudent = studentcheck.objects.filter(SecondweekCheck="尚未簽到")
    elif week == '3':
        uncheckedstudent = studentcheck.objects.filter(ThirdweekCheck="尚未簽到")
    else:
        uncheckedstudent = studentcheck.objects.filter(ForthweekCheck="尚未簽到")

    print(uncheckedstudent.count())
    for i in uncheckedstudent:
        uncheckedstudentname.append(i.cName)

    print(uncheckedstudentname)

    return JsonResponse({'result': uncheckedstudentname})

# 將狀態切換至點名
def changesectiontostudentcheck(request):

    global section
    zenbo = request.GET.get('zenbo')
    if zenbo == '1':
        section[0] = 'studentcheck'
        print("Zenbo 1 Change section to " + section[0])
        print(section)
    elif zenbo == '2':
        section[1] = 'studentcheck'
        print("Zenbo 2 Change section to " + section[1])
        print(section)
    elif zenbo == '3':
        section[2] = 'studentcheck'
        print("Zenbo 3 Change section to " + section[2])
        print(section)
    elif zenbo == '4':
        section[3] = 'studentcheck'
        print("Zenbo 4 Change section to " + section[3])
        print(section)
    elif zenbo == '5':
        section[4] = 'studentcheck'
        print("Zenbo 5 Change section to " + section[4])
        print(section)
    elif zenbo == 'all':
        section = ['studentcheck', 'studentcheck', 'studentcheck', 'studentcheck', 'studentcheck']
        print("All zenbo Change section to " + section[4])
        print(section)

    return JsonResponse({'my_string': "切換為學生簽到模式"})

# 將狀態切換至before you read
def changesectiontobeforeyouread(request):

    global section
    zenbo = request.GET.get('zenbo')
    if zenbo == '1':
        section[0] = 'beforeyouread'
        print("Zenbo 1 Change section to " + section[0])
        print(section)
    elif zenbo == '2':
        section[1] = 'beforeyouread'
        print("Zenbo 2 Change section to " + section[1])
        print(section)
    elif zenbo == '3':
        section[2] = 'beforeyouread'
        print("Zenbo 3 Change section to " + section[2])
        print(section)
    elif zenbo == '4':
        section[3] = 'beforeyouread'
        print("Zenbo 4 Change section to " + section[3])
        print(section)
    elif zenbo == '5':
        section[4] = 'beforeyouread'
        print("Zenbo 5 Change section to " + section[4])
        print(section)
    elif zenbo == 'all':
        section = ['beforeyouread', 'beforeyouread', 'beforeyouread',
                   'beforeyouread', 'beforeyouread']
        print("All zenbo Change section to " + section[4])
        print(section)

    return JsonResponse({'my_string': "切換為Before you read模式"})

# 將狀態切換至vocabulary preview
def changesectiontovocabularypreview(request):

    global section
    unit = request.GET.get('unit')
    reading = request.GET.get('reading')
    zenbo = request.GET.get('zenbo')
    if unit == '10' and reading == '1':
        if zenbo == '1':
            section[0] = 'U10R1vocabularypreview'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R1vocabularypreview'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R1vocabularypreview'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R1vocabularypreview'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R1vocabularypreview'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R1vocabularypreview', 'U10R1vocabularypreview', 'U10R1vocabularypreview', 'U10R1vocabularypreview', 'U10R1vocabularypreview']
            print("All zenbo Change section to " + section[4])
            print(section)
    elif unit == '10' and reading == '2':
        if zenbo == '1':
            section[0] = 'U10R2vocabularypreview'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R2vocabularypreview'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R2vocabularypreview'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R2vocabularypreview'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R2vocabularypreview'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R2vocabularypreview', 'U10R2vocabularypreview', 'U10R2vocabularypreview',
                       'U10R2vocabularypreview', 'U10R2vocabularypreview']
            print("All zenbo Change section to " + section[4])
            print(section)

    return JsonResponse({'my_string': "切換為vocabulary preview模式"})

# 將狀態切換至focus on content
def changesectiontofocusoncontent(request):

    global section
    unit = request.GET.get('unit')
    reading = request.GET.get('reading')
    zenbo = request.GET.get('zenbo')
    if unit == '10' and reading == '1':
        if zenbo == '1':
            section[0] = 'U10R1focusoncontent'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R1focusoncontent'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R1focusoncontent'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R1focusoncontent'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R1focusoncontent'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R1focusoncontent', 'U10R1focusoncontent', 'U10R1focusoncontent', 'U10R1focusoncontent', 'U10R1focusoncontent']
            print("All zenbo Change section to " + section[4])
            print(section)
    elif unit == '10' and reading == '2':
        if zenbo == '1':
            section[0] = 'U10R2focusoncontent'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R2focusoncontent'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R2focusoncontent'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R2focusoncontent'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R2focusoncontent'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R2focusoncontent', 'U10R2focusoncontent', 'U10R2focusoncontent', 'U10R2focusoncontent', 'U10R2focusoncontent']
            print("All zenbo Change section to " + section[4])
            print(section)

    return JsonResponse({'my_string': "切換為focus on content模式"})

# 將狀態切換至vocabulary review
def changesectiontovocabularyreview(request):

    global section
    unit = request.GET.get('unit')
    reading = request.GET.get('reading')
    zenbo = request.GET.get('zenbo')
    if unit == '10' and reading == '1':
        if zenbo == '1':
            section[0] = 'U10R1vocabularyreview'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R1vocabularyreview'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R1vocabularyreview'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R1vocabularyreview'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R1vocabularyreview'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R1vocabularyreview', 'U10R1vocabularyreview', 'U10R1vocabularyreview', 'U10R1vocabularyreview', 'U10R1vocabularyreview']
            print("All zenbo Change section to " + section[4])
            print(section)
    elif unit == '10' and reading == '2':
        if zenbo == '1':
            section[0] = 'U10R2vocabularyreview'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R2vocabularyreview'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R2vocabularyreview'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R2vocabularyreview'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R2vocabularyreview'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R2vocabularyreview', 'U10R2vocabularyreview', 'U10R2vocabularyreview', 'U10R2vocabularyreview', 'U10R2vocabularyreview']
            print("All zenbo Change section to " + section[4])
            print(section)

    return JsonResponse({'my_string': "切換為vocabulary review模式"})

# 將狀態切換至Critical thinking
def changesectiontocriticalthinking(request):

    global section
    zenbo = request.GET.get('zenbo')
    if zenbo == '1':
        section[0] = 'criticalthinking'
        print("Zenbo 1 Change section to " + section[0])
        print(section)
    elif zenbo == '2':
        section[1] = 'criticalthinking'
        print("Zenbo 2 Change section to " + section[1])
        print(section)
    elif zenbo == '3':
        section[2] = 'criticalthinking'
        print("Zenbo 3 Change section to " + section[2])
        print(section)
    elif zenbo == '4':
        section[3] = 'criticalthinking'
        print("Zenbo 4 Change section to " + section[3])
        print(section)
    elif zenbo == '5':
        section[4] = 'criticalthinking'
        print("Zenbo 5 Change section to " + section[4])
        print(section)
    elif zenbo == 'all':
        section = ['criticalthinking', 'criticalthinking', 'criticalthinking',
                   'criticalthinking', 'criticalthinking']
        print("All zenbo Change section to " + section[4])
        print(section)

    return JsonResponse({'my_string': "切換為Critical Thinking模式"})

# 確認各組學生都已簽到完成
def groupcheckok(request):

    global section
    group = request.GET.get('group')
    week = request.GET.get('week')
    if group == '1':
        section[0] = "section"
    elif group == '2':
        section[1] = "section"
    elif group == '3':
        section[2] = "section"
    elif group == '4':
        section[3] = "section"
    elif group == '5':
        section[4] = "section"
    else:
        section = ["section", "section", "section", "section", "section"]

    return JsonResponse({"": "Done"})

# 回傳各組所屬狀態至Zenbo Junior
def checksection(request):

    global section
    zenbo = request.GET.get('zenbo')
    if zenbo == '1':
        return JsonResponse({"section": section[0]})
    elif zenbo == '2':
        return JsonResponse({"section": section[1]})
    elif zenbo == '3':
        return JsonResponse({"section": section[2]})
    elif zenbo == '4':
        return JsonResponse({"section": section[3]})
    elif zenbo == '5':
        return JsonResponse({"section": section[4]})
    else:
        return JsonResponse({"": "Error"})

# 回傳相應學號的vocabulary preview成績
def getvocabularypreviewscoreNET(request):

    try:
        cId = request.GET.get('cId')
        reading = request.GET.get('reading')
        student = studentcheck.objects.get(cId=cId)
        if reading == '1':
            point = str(student.vp1point)+"pts"
            return JsonResponse({"": point})
        elif reading == '2':
            point = str(student.vp2point) + "pts"
            return JsonResponse({"": point})
    except:
        point = "Error"
        return JsonResponse({"": point})
        print("Error")

# 回傳相應學號的vocabulary review成績
def getvocabularyreviewscoreNET(request):

    try:
        cId = request.GET.get('cId')
        reading = request.GET.get('reading')
        student = studentcheck.objects.get(cId=cId)
        if reading == '1':
            point = str(student.vr1point) + "pts"
            return JsonResponse({"": point})
        elif reading == '2':
            point = str(student.vr2point) + "pts"
            return JsonResponse({"": point})
    except:
        point = "Error"
        return JsonResponse({"": point})
        print("Error")

# 回傳相應學號的focus on content成績
def getfocusoncontentscoreNET(request):

    try:
        cId = request.GET.get('cId')
        reading = request.GET.get('reading')
        student = studentcheck.objects.get(cId=cId)
        if reading == '1':
            point = str(student.foc1point) + "pts"
            return JsonResponse({"": point})
        elif reading == '2':
            point = str(student.foc2point) + "pts"
            return JsonResponse({"": point})
    except:
        point = "Error"
        return JsonResponse({"": point})
        print("Error")

# 回傳單字詞性及英文解釋
def getvocabularydetailNET(request):

    global vocabularylist
    vocabularylist.clear()
    i = 0
    unit = request.GET.get('unit')
    reading = request.GET.get('reading')
    vocabularyarray = VocabularyDetail.objects.filter(unit=unit, reading=reading)
    for vocabulary in vocabularyarray:
        vocabularylist.append(str(vocabulary))
        print(str(vocabulary))
    return JsonResponse({'v1': vocabularylist[0], 'v2': vocabularylist[1], 'v3': vocabularylist[2]
                         , 'v4': vocabularylist[3], 'v5': vocabularylist[4], 'v6': vocabularylist[5]
                         , 'v7': vocabularylist[6], 'v8': vocabularylist[7]})

# 回傳相應學生vocabulary preview的作答記錄
def getvocabularypreviewanswerNET(request):

    reading = request.GET.get('reading')
    cId = request.GET.get('cId')
    if reading == '1':
        studentdetail = U10R1VocabularyPreviewAns.objects.filter(cId=cId).first()
    else:
        studentdetail = U10R2VocabularyPreviewAns.objects.filter(cId=cId).first()
    correctans = VocabularyPreview.objects.filter(reading=reading)
    questionset = VocabularyPreview.objects.filter(reading=reading).order_by('questionnum')
    return JsonResponse({'cId': studentdetail.cId, 'Q1': questionset[0].question, 'Q2': questionset[1].question
                         , 'Q3': questionset[2].question, 'Q4': questionset[3].question, 'Q5': questionset[4].question
                         , 'Q6': questionset[5].question, 'Q7': questionset[6].question, 'Q8': questionset[7].question
                         , 'q1answer': studentdetail.q1answer, 'q2answer': studentdetail.q2answer
                         , 'q3answer': studentdetail.q3answer, 'q4answer': studentdetail.q4answer, 'q5answer': studentdetail.q5answer
                         , 'q6answer': studentdetail.q6answer, 'q7answer': studentdetail.q7answer, 'q8answer': studentdetail.q8answer
                         , 'q1coranswer': correctans[0].correctans, 'q2coranswer': correctans[1].correctans, 'q3coranswer': correctans[2].correctans
                         , 'q4coranswer': correctans[3].correctans, 'q5coranswer': correctans[4].correctans, 'q6coranswer': correctans[5].correctans
                         , 'q7coranswer': correctans[6].correctans, 'q8coranswer': correctans[7].correctans, 'point': studentdetail.point})

# 回傳相應學生vocabulary review的作答記錄
def getvocabularyreviewanswerNET(request):

    reading = request.GET.get('reading')
    cId = request.GET.get('cId')
    if reading == '1':
        studentdetail = U10R1VocabularyReviewAns.objects.filter(cId=cId).first()
    else:
        studentdetail = U10R2VocabularyReviewAns.objects.filter(cId=cId).first()
    correctans = VocabularyReview.objects.filter(reading=reading)
    questionset = VocabularyReview.objects.filter(reading=reading).order_by('questionnum')
    return JsonResponse({'cId': studentdetail.cId, 'Q1': questionset[0].question, 'Q2': questionset[1].question
                         , 'Q3': questionset[2].question, 'Q4': questionset[3].question, 'Q5': questionset[4].question
                         , 'Q6': questionset[5].question, 'Q7': questionset[6].question, 'Q8': questionset[7].question
                         , 'q1answer': studentdetail.q1answer, 'q2answer': studentdetail.q2answer, 'q3answer': studentdetail.q3answer
                         , 'q4answer': studentdetail.q4answer, 'q5answer': studentdetail.q5answer, 'q6answer': studentdetail.q6answer
                         , 'q7answer': studentdetail.q7answer, 'q8answer': studentdetail.q8answer
                         , 'q1coranswer': correctans[0].correctans, 'q2coranswer': correctans[1].correctans, 'q3coranswer': correctans[2].correctans
                         , 'q4coranswer': correctans[3].correctans, 'q5coranswer': correctans[4].correctans, 'q6coranswer': correctans[5].correctans
                         , 'q7coranswer': correctans[6].correctans, 'q8coranswer': correctans[7].correctans, 'point': studentdetail.point})

# 記錄學生在critical thinking的作答
def criticalthinkingrecord(request):

    cId = request.GET.get('cId')
    choose = request.GET.get('choose')
    beforeorafter = request.GET.get('time')
    student = studentcheck.objects.get(cId=cId)
    if choose == 'affirmative':
        if beforeorafter == 'before':
            student.ctchoosebeforediscuss = 1
        elif beforeorafter == 'after':
            student.ctchooseafterdiscuss = 1
    elif choose == 'negative':
        if beforeorafter == 'before':
            student.ctchoosebeforediscuss = -1
        elif beforeorafter == 'after':
            student.ctchooseafterdiscuss = -1
    student.save()

    return JsonResponse({'result': "Good Job"})

# Zenbo Junior 選完組別後回傳該組學生名單
def getgroupstudents(request):

    group = request.GET.get('group')
    students = studentcheck.objects.all()
    if group == "1":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    elif group == "2":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    elif group == "3":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    elif group == "4":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    elif group == "5":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    else:
        students = studentcheck.objects.filter(cGroup=group).order_by('id')

    if students.count() == 4:
        return JsonResponse(
            {'student1': students[0].cId, 'student2': students[1].cId, 'student3': students[2].cId,
             'student4': students[3].cId})
    elif students.count() == 5:
        return JsonResponse(
            {'student1': students[0].cId, 'student2': students[1].cId, 'student3': students[2].cId,
             'student4': students[3].cId, 'student5': students[4].cId, 'student6': "student"})
    else:
        return JsonResponse(
            {'student1': students[0].cId, 'student2': students[1].cId, 'student3': students[2].cId,
             'student4': students[3].cId, 'student5': students[4].cId, 'student6': students[5].cId})

# 授課教師匯入後的單字教學
def teachcustomizevocabulary(request):
    package = request.GET.get('package')
    if package != None:
        Vocabularies = CustomizeVocabulary.objects.filter(package=package)
    categories = []
    packagename = ""
    randomset = CustomizeVocabulary.objects.filter(~Q(package=packagename)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(package=packagename)).order_by('id')
        randomone = randomset.first()
        packagename = randomone.package
        categories.append(packagename)
        if randomset.filter(~Q(package=packagename)).count() == 0:
            break

    return render(request, "TeachCustomizeVocabulary.html", locals())

# 授課教師匯入名單後的點名系統
def customizestudentslist(request):
    classid = request.GET.get('classid')
    if classid != None:
        StudentsList = CustomizeStudentList.objects.filter(classid=classid)
        serializersstudentlist = serializers.serialize("json", StudentsList)
    classids = []
    classidname = ""
    randomset = CustomizeStudentList.objects.filter(~Q(classid=classidname)).order_by('id')
    while 1 :
        randomset = randomset.filter(~Q(classid=classidname)).order_by('id')
        randomone = randomset.first()
        classidname = randomone.classid
        classids.append(classidname)
        if randomset.filter(~Q(classid=classidname)).count()==0:
            break

    return render(request, "CustomizeStudents.html", locals())

# 授課教師匯入名單後加減分
def customizestudentchangepoint(request):
    studentid = request.GET.get('student')
    plusorminus = request.GET.get('change')
    student = CustomizeStudentList.objects.get(studentid=studentid)
    if plusorminus == "plus":
        student.studentpoint += 1
    else:
        student.studentpoint -= 1
    student.save()
    return JsonResponse({'responsemessage': "Success"})

# 授課教師匯入名單後更改簽到狀況
def customizestudentchangecheck(request):
    studentid = request.GET.get('student')
    student = CustomizeStudentList.objects.get(studentid=studentid)
    if student.studentcheck == "尚未簽到":
        student.studentcheck = "已簽到"
    else:
        student.studentcheck = "尚未簽到"
    student.save()
    return JsonResponse({'responsemessage': 'Success'})

# 授課教師匯入名單後隨機點名
def customizerandompickstudent(request):
    group = request.GET.get('group')
    classid = request.GET.get('classid')
    if group == "all":
        pickedstudent = CustomizeStudentList.objects.filter(classid=classid).order_by('?').first()
    else:
        pickedstudent = CustomizeStudentList.objects.filter(classid=classid, studentgroup=group).order_by('?').first()
    return JsonResponse({'pickedstudent': pickedstudent.studentname})

# Create your views here.