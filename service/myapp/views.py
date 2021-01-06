from django.shortcuts import render
from .models import Pay,studentcheck
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .models import studentcheck
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

def hello3(request,username):
    now = datetime.now()
    return render(request,"hello3.html",locals())

@csrf_exempt
def hello4(request):
    now = datetime.now()
    checkunit = request.GET.get('unit')
    print(checkunit)
    checklesson = request.GET.get('lesson')
    print(checklesson)
    return render(request,"hello4.html",locals())

def uncheckedstudentNET(request):
    try:
        uncheckedstudent = studentcheck.objects.get(FirstweekCheck="0")
    except:
        errormessage = " (讀取錯誤 !)"
    return render(request,"uncheckedstudent.html", locals())

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

        while True:
            conn, addr = client.accept()
            print("client with address: ", addr, " is connected.")
            data = "hello"
            data = conn.recv(1024)
            print("Recieved this data: <", data.decode(), "> from the client.")
            print(data)

            if data.decode() == "hahaha":
                reply = "Success"
                conn.send(reply.encode("utf-8"))
                conn.close()
                print("-----------------------------")

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

    recv()

# Create your views here.

