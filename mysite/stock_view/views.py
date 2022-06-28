from django.shortcuts import redirect, render,HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from stock_view.models import UserInfo, TradeInfo
from django.contrib import messages
from stock_view.models import StockInfo
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

# def Allrank(request):
#     objs=StockInfo.objects.all()
#     return render(request,"general.html",locals())

def Allrank(request):
    return render(request,"Allrank.html",{'data':[{'no':stock.no,'id':stock.stock_id,'name':stock.stock_name,
    'price':stock.now_price,'changepercent':stock.changepercent,'changeamount':stock.changeamount,
    'turnover':stock.turnover,'vol':stock.vol,'swing':stock.swing,'high_price':stock.high_price,
    'low_price':stock.low_price,'open_price':stock.open_price,'close_price_yesterday':stock.close_price_yesterday,
    'quantity_relative_ratio':stock.quantity_relative_ratio,'turnover_rate':stock.turnover_rate,'pe':stock.pe,
    'pb':stock.pb,'total_value':stock.total_value,'higher_speed':stock.higher_speed,
    'five_min_up_down':stock.five_min_up_down,'sixty_day_up_down':stock.sixty_day_up_down,
    'yeartodate_up_down':stock.yeartodate_up_down} for stock in StockInfo.objects.all()]})


def test(request):
    return render(request,"test.html",{"a":[1,2,3,4,5,6]})


def trl(request):
    trade_list = TradeInfo.objects.all()

    return render(request,"trade_ranking_list.html",{"trade_list":trade_list})