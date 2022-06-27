from django.shortcuts import redirect, render,HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from stock_view.models import UserInfo, TradeInfo
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,"index.html")

def user_list(request):
    return render(request,"user_list.html")

def user_add(request):
    return HttpResponse("添加用户")

@csrf_exempt
def login(request):
    if(request.method=="GET"):
        return render(request,"login.html")
    Nam=request.POST.get('account')
    pwd=request.POST.get('password')
    name_obj=UserInfo.objects.filter(name=Nam,password=pwd)
    if(len(name_obj)!=0):
        return redirect(index)
    else:
        return render(request,"login.html",{"error_msg":"用户名或密码错误"})

@csrf_exempt
def register(request):
    if(request.method=="GET"):
        return render(request,"register.html")
    Name=request.POST.get('account')
    pwd=request.POST.get('password')
    again_pass=request.POST.get('again_pass')
    name_obj=UserInfo.objects.filter(name=Name)
    if(len(name_obj)!=0):
         return render(request,"register.html",{"error_msg1":"用户名已存在"})
    elif(pwd!=again_pass):
        return render(request,"register.html",{"error_msg2":"两次密码不一致"})
    else:
        UserInfo.objects.create(name=Name,password=pwd)
        messages.success(request, '注册成功')
        return redirect(login)
    
def test(request):
    return render(request,"test.html",{"a":[1,2,3,4,5,6]})


def trl(request):
    trade_list = TradeInfo.objects.all()

    return render(request,"trade_ranking_list.html",{"trade_list":trade_list})