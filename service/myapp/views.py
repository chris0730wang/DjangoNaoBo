from django.shortcuts import render, redirect
from .models import Pay,studentcheck,VocabularyPreview,VocabularyPreviewAns,BeforeYouRead,U5BeforeYouReadAns
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

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

def sayhello(request):

    return HttpResponse("Hello django !")

def hello2(request,username):

    return HttpResponse("Hello " + username)

def naoindexNET(request):
    return render(request, "naoindex.html", locals())
@csrf_exempt
def hello4(request):

    now = datetime.now()
    checkunit = request.GET.get('unit')
    print(checkunit)
    checkreading = request.GET.get('reading')
    print(checkreading)
    return render(request,"hello4.html",locals())

def checkstudentNET(request):

    try:
        checkedstudent1 = studentcheck.objects.filter(cGroup='1').order_by('id')
        checkedstudent2 = studentcheck.objects.filter(cGroup='2').order_by('id')
        checkedstudent3 = studentcheck.objects.filter(cGroup='3').order_by('id')
        checkedstudent4 = studentcheck.objects.filter(cGroup='4').order_by('id')
    except:
        errormessage = " (讀取錯誤 !)"
    return render(request, "uncheckedstudent.html", locals())

def editcheck(request):

    cId = request.GET.get('cId')
    print(cId)

    t = studentcheck.objects.get(cId=cId)
    try:
        if t.FirstweekCheck == '已簽到':
            t.FirstweekCheck = '尚未簽到'
            t.save()
            return redirect('/checkstudent/')
        if t.FirstweekCheck == '尚未簽到':
            t.FirstweekCheck = '已簽到'
            t.save()
            return redirect('/checkstudent/')
    except:
        return redirect('/checkstudent/')

def studentcheckNET(request):

    cId = request.GET.get('cId')
    print(cId)
    week = request.GET.get('week')
    print(week)
    try:
        t = studentcheck.objects.get(cId=cId)
        if week == '1':
            t.FirstweekCheck = "已簽到"
        if week == '2':
            t.SecondweekCheck = '1'
        if week == '3':
            t.ThirdweekCheck = '1'
        if week == '4':
            t.ForthweekCheck = '1'
        t.save()
        return HttpResponse("check_ok")
    except ObjectDoesNotExist:
        return HttpResponse("check_error")

def pluspointNET(request):

    cId = request.GET.get('cId')
    print(cId)
    try:
        t = studentcheck.objects.get(cId=cId)
        t.point += 1
        t.save()
        return redirect('/checkstudent/')
    except:
        return redirect('/checkstudent/')

def subpointNET(request):

    cId = request.GET.get('cId')
    print(cId)
    try:
        t = studentcheck.objects.get(cId=cId)
        t.point -= 1
        t.save()
        return redirect('/checkstudent/')
    except:
        return redirect('/checkstudent/')

def randompickstudentNET(request):

    group = request.GET.get('group')
    week = request.GET.get('week')

    try:
        if week == '1':
            t = studentcheck.objects.filter(cGroup=group, FirstweekCheck="已簽到", picked=0).order_by('?').first()
        elif week == '2':
            t = studentcheck.objects.filter(cGroup=group, secondweekcheck="已簽到", picked=0).order_by('?').first()
        elif week == '3':
            t = studentcheck.objects.filter(cGroup=group, thirdweekcheck="已簽到", picked=0).order_by('?').first()
        elif week == '4':
            t = studentcheck.objects.filter(cGroup=group, forthweekcheck="已簽到", picked=0).order_by('?').first()

        t.picked = 1
        t.save()

        return JsonResponse({'my_string': t.cName})
    except:
        return JsonResponse({'my_string': '每位學生都已抽點過'})

def beforeyoureadNET(request):

    try:
        unit = request.GET.get('unit')
        if unit == '5':
            for i in range(1, 6):
                if i == 1:
                    question = BeforeYouRead.objects.get(unit=unit, number=1)
                    studentans = U5BeforeYouReadAns.objects.filter(q1answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q1answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q1answer=question.option3)
                    question.numof3 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q1answer=question.option4)
                    question.numof4 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q1answer=question.option5)
                    question.numof5 = studentans.count()
                    question.save()
                elif i == 2:
                    question = BeforeYouRead.objects.get(unit=unit, number=2)
                    studentans = U5BeforeYouReadAns.objects.filter(q2answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q2answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q2answer=question.option3)
                    question.numof3 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q2answer=question.option4)
                    question.numof4 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q2answer=question.option5)
                    question.numof5 = studentans.count()
                    question.save()
                elif i == 3:
                    question = BeforeYouRead.objects.get(unit=unit, number=3)
                    studentans = U5BeforeYouReadAns.objects.filter(q3answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q3answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q3answer=question.option3)
                    question.numof3 = studentans.count()
                    question.save()
                elif i == 4:
                    question = BeforeYouRead.objects.get(unit=unit, number=4)
                    studentans = U5BeforeYouReadAns.objects.filter(q4answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q4answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q4answer=question.option3)
                    question.numof3 = studentans.count()
                    question.save()
                elif i == 5:
                    question = BeforeYouRead.objects.get(unit=unit, number=5)
                    studentans = U5BeforeYouReadAns.objects.filter(q5answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q5answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U5BeforeYouReadAns.objects.filter(q5answer=question.option3)
                    question.numof3 = studentans.count()
                    question.save()

    except:
        print("error")
    return render(request, "beforeyoureadresult.html", locals())

def vocabularypreviewresultNET(request):

    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        correctansset = VocabularyPreview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
        numofansstudent = studentans.count()
        for i in range(1, 9):
            correctans = VocabularyPreview.objects.get(unit=unit, reading=reading, questionnum=i)
            if i == 1:
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                correctans.numof1 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                correctans.numof2 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                correctans.numof3 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
            elif i == 2:
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                correctans.numof1 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                correctans.numof2 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                correctans.numof3 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
            elif i == 3:
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                correctans.numof1 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                correctans.numof2 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                correctans.numof3 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
            elif i == 4:
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                correctans.numof1 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                correctans.numof2 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                correctans.numof3 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
            elif i == 5:
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                correctans.numof1 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                correctans.numof2 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                correctans.numof3 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
            elif i == 6:
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                correctans.numof1 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                correctans.numof2 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                correctans.numof3 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
            elif i == 7:
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                correctans.numof1 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                correctans.numof2 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                correctans.numof3 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
            elif i == 8:
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                correctans.numof1 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                correctans.numof2 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                correctans.numof3 = studentans.count()
                studentans = VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
            correctans.save()
    except:
        print("error ! ")
        errormessage = "Error !"
    return render(request, "vocabularypreviewresult.html", locals())

def socket(request):

    import socket
    host, port = "140.134.26.196", 1234
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recv():
        try:
            client.bind((host, port))
        finally:
            pass
        client.listen(10)  # how many connections can it receive at one time
        print("Start Listening...")
        clientnum = 0

        while True:
            if clientnum == 2:
                client.close()

            conn, addr = client.accept()
            print("client with address: ", addr, " is connected.")
            data = conn.recv(1024)
            print("Recieved this data: <", data.decode(), "> from the client.")
            print(data)


            if data.decode() == "hahaha":
                reply = "Success"
                conn.send(reply.encode("utf-8"))
                conn.close()
                print("-----------------------------")
                clientnum = clientnum + 1


            elif data.decode() == "Disconnect":
                reply = "Disconnected and the listen has Stopped"
                conn.send(reply.encode("utf-8"))
                conn.close()
                break
            else:
                reply = "hello"
                conn.send(reply.encode("utf-8"))
                conn.close()
                print("-----------------------------")

        client.close()
    print("hello")
    recv()

# Create your views here.

