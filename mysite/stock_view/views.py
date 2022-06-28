from django.shortcuts import redirect, render,HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from stock_view.models import UserInfo
from stock_view.code.get_now_data import get_1a0001
from django.contrib import messages
# Create your views here.
def index(request):
    shang_time,shang_value=get_1a0001()
    shang_time[0]='0930'
    
    for i in range(0,len(shang_time)):
        a=list(shang_time[i])
        # a.insert(-2,':')
        shang_time[i]=''.join(a)
    print(shang_time)
    shang_value =list(map(float,shang_value))
    return render(request,"index.html",locals())

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
    shang_time,shang_value=get_1a0001()
    shang_time[0]='0930'
    
    for i in range(0,len(shang_time)):
        a=list(shang_time[i])
        a.insert(-2,':')
        shang_time[i]=''.join(a)
    print(shang_time)
    shang_value =list(map(float,shang_value))
    return render(request,"test.html",locals())