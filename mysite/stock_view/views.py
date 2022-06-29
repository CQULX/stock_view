from django.http import JsonResponse
from django.shortcuts import redirect, render,HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from stock_view.models import StockExternal, UserInfo
from stock_view.code.get_now_data import get_1a0001
from stock_view.models import UserInfo, TradeInfo
from django.contrib import messages
from stock_view.models import StockInfo
from stock_view.models import Favorite
from stock_view.code.get_now_data import get_1a0001,get_399001,get_399006,get_numUpAndDown
# Create your views here.
def index(request):

    shang_time,shang_value=get_1a0001()
    shang_time[0]='0930'
    shen_time,shen_value=get_399001()
    shen_time[0]='0930'
    chuang_time,chuang_value=get_399006()
    chuang_time[0]='0930'
    up_and_down=get_numUpAndDown()
    # for i in range(0,len(shang_time)):
    #     a=list(shang_time[i])
    #     # a.insert(-2,':')
    #     shang_time[i]=''.join(a)
    # print(shang_time)
    shang_value =list(map(float,shang_value))
    shen_value =list(map(float,shen_value))
    chuang_value =list(map(float,chuang_value))
    stock_sum=0
    for x in up_and_down:
        stock_sum=stock_sum+x
    up_rate=(up_and_down[0]+up_and_down[1]+up_and_down[2])/stock_sum
    down_rate=(up_and_down[3]+up_and_down[4]+up_and_down[5])/stock_sum
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
    shang_time,shang_value=get_1a0001()
    shang_time[0]='0930'
    
    for i in range(0,len(shang_time)):
        a=list(shang_time[i])
        a.insert(-2,':')
        shang_time[i]=''.join(a)
    print(shang_time)
    shang_value =list(map(float,shang_value))
    return render(request,"test.html",locals())


def trl(request):
    trade_list = TradeInfo.objects.all()

    return render(request,"trade_ranking_list.html",{"trade_list":trade_list})

def stock_search(request):
    id_name={}
    stock_name=[]
    for stock in StockInfo.objects.all():
        id_name[stock.stock_id]=stock.stock_name
        stock_name.append(stock.stock_name)
    print(stock_name)
    return render(request,"stock_search.html",locals())

def rankByMap(request):
    address={str(i.stock_id).zfill(6):i.stock_address for i in StockExternal.objects.all()}
    return render(request,"rankByMap.html",{'data':[{'no':stock.no,'id':stock.stock_id,'name':stock.stock_name,
    'price':stock.now_price,'changepercent':stock.changepercent,'changeamount':stock.changeamount,
    'turnover':stock.turnover,'vol':stock.vol,'swing':stock.swing,'high_price':stock.high_price,
    'low_price':stock.low_price,'open_price':stock.open_price,'close_price_yesterday':stock.close_price_yesterday,
    'quantity_relative_ratio':stock.quantity_relative_ratio,'turnover_rate':stock.turnover_rate,'pe':stock.pe,
    'pb':stock.pb,'total_value':stock.total_value,'higher_speed':stock.higher_speed,
    'five_min_up_down':stock.five_min_up_down,'sixty_day_up_down':stock.sixty_day_up_down,
    'yeartodate_up_down':stock.yeartodate_up_down,'address':address.get(stock.stock_id)} for stock in StockInfo.objects.all()]})


def rankByTrade(request):
    industry={str(i.stock_id).zfill(6):i.stock_industry for i in StockExternal.objects.all()}
    return render(request,"rankByTrade.html",{'data':[{'no':stock.no,'id':stock.stock_id,'name':stock.stock_name,
    'price':stock.now_price,'changepercent':stock.changepercent,'changeamount':stock.changeamount,
    'turnover':stock.turnover,'vol':stock.vol,'swing':stock.swing,'high_price':stock.high_price,
    'low_price':stock.low_price,'open_price':stock.open_price,'close_price_yesterday':stock.close_price_yesterday,
    'quantity_relative_ratio':stock.quantity_relative_ratio,'turnover_rate':stock.turnover_rate,'pe':stock.pe,
    'pb':stock.pb,'total_value':stock.total_value,'higher_speed':stock.higher_speed,
    'five_min_up_down':stock.five_min_up_down,'sixty_day_up_down':stock.sixty_day_up_down,
    'yeartodate_up_down':stock.yeartodate_up_down,'industry':industry.get(stock.stock_id)} for stock in StockInfo.objects.all()]})

@csrf_exempt
def starbox(request):
    star_list=Favorite.objects.all()
    return render(request, "starbox.html", {"star_list": star_list})

@csrf_exempt
# 根据id列表批量删除数据
def deleteProductByIdList(request):
    mod = Favorite.objects
    # 获取前端传来的id数组
    idlist = request.GET.getlist('ids[]')
    try:
        # 遍历id数组
        for id in idlist:
            # 删除对应id的记录
            mod.get(id=id).delete()
        context = {"info": "删除成功"}
    except Exception as res:
        context = {"info": str(res)}
    return JsonResponse({"msg": context})

def get_trade(request,param1):
    star_list=Favorite.objects.all()
    return redirect(index)



