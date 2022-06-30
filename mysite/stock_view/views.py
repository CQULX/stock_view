
from logging import Manager

from turtle import st

from django.http import JsonResponse
from django.shortcuts import redirect, render,HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from stock_view.models import StockExternal, UserInfo
from stock_view.code.get_now_data import get_1a0001
from stock_view.models import UserInfo, TradeInfo,StockHisinfo,StockExternal
from django.contrib import messages

from stock_view.models import StockInfo,CompanyInfo1
from stock_view.models import Favorite,ManagerInfo

from stock_view.models import StockInfo
from stock_view.models import Favorite
import math
from stock_view.code.get_stock_info import update
from stock_view.code.get_now_data import get_1a0001,get_399001,get_399006,get_numUpAndDown

# Create your views here.

def checkLogin(func):
    def warpper(request,*args,**kwargs):
        if request.session.get('login_user', False):
            return func(request, *args, **kwargs)
        else:
            return redirect('/gotologin')
    return warpper

@checkLogin
def index(request):
    stock_count=StockExternal.objects.all().count()
    company_count=CompanyInfo1.objects.all().count()
    user_count=UserInfo.objects.all().count()
    trade_count=TradeInfo.objects.all().count()
    shang_time,shang_value=get_1a0001()
    shang_time[0]='0930'
    shen_time,shen_value=get_399001()
    shen_time[0]='0930'
    chuang_time,chuang_value=get_399006()
    chuang_time[0]='0930'
    shang_value =list(map(float,shang_value))
    shen_value =list(map(float,shen_value))
    chuang_value =list(map(float,chuang_value))
    up_and_down=get_numUpAndDown()
    stock_sum=0
    for x in up_and_down:
        stock_sum=stock_sum+x
    up_rate=(up_and_down[0]+up_and_down[1]+up_and_down[2])/stock_sum
    down_rate=(up_and_down[3]+up_and_down[4]+up_and_down[5])/stock_sum
    # for i in range(0,len(shang_time)):
    #     a=list(shang_time[i])
    #     # a.insert(-2,':')
    #     shang_time[i]=''.join(a)
    # print(shang_time)
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
        request.session['login_user']={
                                'user_name':Nam,
                                'user_id' :UserInfo.objects.get(name=Nam).id,
                                'isManager':UserInfo.objects.get(name=Nam).isManager,
                                'isSuperManager':UserInfo.objects.get(name=Nam).isSuperManager,
                            }
        request.session['login_user']['YesOrNoManager']="yes" if request.session['login_user']['isManager'] == b'\x01' else "no"
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
@checkLogin
def Allrank(request):
    return render(request,"Allrank.html",{'data':[{'no':stock.no,'id':stock.stock_id,'name':stock.stock_name,
    'price':stock.now_price,'changepercent':stock.changepercent,'changeamount':stock.changeamount,
    'turnover':stock.turnover,'vol':stock.vol,'swing':stock.swing,'high_price':stock.high_price,
    'low_price':stock.low_price,'open_price':stock.open_price,'close_price_yesterday':stock.close_price_yesterday,
    'quantity_relative_ratio':stock.quantity_relative_ratio,'turnover_rate':stock.turnover_rate,'pe':stock.pe,
    'pb':stock.pb,'total_value':stock.total_value,'higher_speed':stock.higher_speed,
    'five_min_up_down':stock.five_min_up_down,'sixty_day_up_down':stock.sixty_day_up_down,
    'yeartodate_up_down':stock.yeartodate_up_down} for stock in StockInfo.objects.all()]})

@checkLogin
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

@checkLogin
def trl(request):
    trade_list = TradeInfo.objects.all()

    return render(request,"trade_ranking_list.html",{"trade_list":trade_list})

@checkLogin
@csrf_exempt
def stock_search(request):
    if(request.method=="GET"):
        return render(request,"stock_search.html")
    STOCK_ID=request.POST.get('myInput')
    print(STOCK_ID)
    return redirect("./"+STOCK_ID)
    


    
    
@checkLogin
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

@checkLogin
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

@checkLogin
@csrf_exempt
def starbox(request):
    Nam=request.session.get('login_user')['user_name']
    star_list=Favorite.objects.filter(username=Nam)
    newstar_list=[{'stock_id':str(i.stock_id).zfill(6),'fav_date':i.fav_date}for i in star_list]
    return render(request, "starbox.html", {"star_list": newstar_list})

@checkLogin
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

@checkLogin
@csrf_exempt
def company_search(request):
    if(request.method=="GET"):
        company_name=[]
        for company in CompanyInfo1.objects.all():
            company_name.append(company.company_name)
        # print(company_name)
        return render(request,"company_search.html",{'company_name':company_name})
    name=request.POST.get('myInput')
    # print(name)
    return redirect("./"+name)

@checkLogin
@csrf_exempt
def company_search_detail(request,id):
    # print(id)
    if(request.method=="POST"):
        name=request.POST.get('myInput')
        return redirect("../"+name)
    company_name=[]
    for company1 in CompanyInfo1.objects.all():
        company_name.append(company1.company_name)
    company=CompanyInfo1.objects.get(company_name=id)
    # print(company.company_name)
    company_info={}
    company_info['company_name']=company.company_name
    company_info['territory']=company.territory
    company_info['industry']=company.industry
    company_info['url']=company.url
    company_info['business']=company.business
    company_info['product']=company.product
    company_info['shareholder']=company.shareholder
    company_info['chairman']=company.chairman
    company_info['board_secretariat']=company.board_secretariat
    company_info['correp']=company.correp
    company_info['generalmanager']=company.generalmanager
    company_info['reg_fund']=company.reg_fund
    company_info['num_employees']=company.num_employees
    company_info['phone']=company.phone
    company_info['fax']=company.fax
    company_info['zipcode']=company.zipcode
    company_info['address']=company.address
    company_info['profile']=company.profile
    manager=['chairman','board_secretariat','correp','generalmanager']
    manager_info=[{},{},{},{}]
    stock=StockExternal.objects.get(company_name=id)
    stock_id=stock.stock_id
    stock_id=str(stock_id).zfill(6)
    print(type(stock_id))
    for i in range(0, len(manager)):
        m1=ManagerInfo.objects.get(manager_name=company_info[manager[i]])
        if m1:
            manager_info[i]['manager_name']=m1.manager_name
            manager_info[i]['manager_gender']=m1.manager_gender
            manager_info[i]['manager_age']=m1.manager_age
            manager_info[i]['manager_edu']=m1.manager_edu
            manager_info[i]['manager_intro']=m1.manager_intro
        else:
            manager_info[i]['manager_name']="暂无信息"
            manager_info[i]['manager_gender']="暂无信息"
            manager_info[i]['manager_age']="暂无信息"
            manager_info[i]['manager_edu']="暂无信息"
            manager_info[i]['manager_intro']="暂无信息"
    # print(company_info)
    return render(request,"company_search_detail.html",{'data':company_info,'manager':manager_info,'stock':stock_id,'company_name':company_name})

def stock_search_detail(request,id):
    if(request.method=="GET"):
        SID=int(id)
        specific_stock=StockInfo.objects.filter(stock_id=id)
        stock_company=StockExternal.objects.filter(stock_id=SID)
        for x in stock_company:
            c_name=x.company_name
            break
        for x in specific_stock:
            s_name=x.stock_name
            s_price=x.now_price
            s_changep=x.changepercent
            s_changea=x.changeamount
            s_changehand=x.turnover_rate
            s_totalvalue=str(round(x.total_value/100000000,2))
            s_traded_market_value=str(round(x.traded_market_value/100000000,2))
            s_swing=x.swing
            s_high_price=x.high_price
            s_low_price=x.low_price
            s_open_price=x.open_price
            s_close_price_yesterday=x.close_price_yesterday
            s_quan_ratio=x.quantity_relative_ratio
            s_PE=x.pe
            s_PB=x.pb
            s_5min_updown=x.five_min_up_down
            s_60day_updown=x.sixty_day_up_down
            s_year_updown=x.yeartodate_up_down
            break
        stock_info=StockHisinfo.objects.filter(stock_id=SID)
        stock_info_list=[]
        for info in stock_info:
            tmp=[]
            tmp.append(str(info.stock_date).replace('-','/'))
            tmp.append(info.open_price)
            tmp.append(info.close_price)
            tmp.append(info.low_price)
            tmp.append(info.high_price)
            stock_info_list.append(tmp)
        name=id+" "+s_name
        return render(request,"stock_search_detail.html",{'name':name,'stock_info_list':stock_info_list,'s_price':s_price,'s_changep':s_changep,'s_changehand':s_changehand,'s_totalvalue':s_totalvalue,
        's_traded_market_value':s_traded_market_value,'s_changea':s_changea,'s_swing':s_swing,'s_high_price':s_high_price,'s_low_price':s_low_price,
        's_open_price':s_open_price,'s_close_price_yesterday':s_close_price_yesterday,'s_quan_ratio':s_quan_ratio,'s_PE':s_PE,'s_PB':s_PB,
        's_5min_updown':s_5min_updown,'s_60day_updown':s_60day_updown,'s_year_updown':s_year_updown,'c_name':c_name})
    STOCK_ID=request.POST.get('myInput')
    return redirect("./"+STOCK_ID)
     

def get_trade(request,param1):
    star_list=Favorite.objects.all()
    return redirect(index)

@checkLogin
def Usersettings(request):
    return render(request,'userSettings.html')

@checkLogin
@csrf_exempt
def UserInfoSet(request):
    mod = UserInfo.objects
    Myid = request.POST.get('id')
    newname = request.POST.get('name')
    print(Myid)
    try:
        mod.filter(id=Myid).update(name=newname)
        context = {"info":"修改成功"}
    except:
        context = {"info":"修改失败"}
    return JsonResponse({"msg": context})

@checkLogin
@csrf_exempt
def changeMyPassword(request):
    mod = UserInfo.objects
    Myid = request.POST.get('id')
    print(Myid)
    oldpassword = request.POST.get('oldpassword')
    newpassword = request.POST.get('newpassword')
    name_obj=UserInfo.objects.filter(id=Myid,password=oldpassword)
    if len(name_obj)==0:
        return JsonResponse({"msg":{"info":"密码错误"}})
    try:
        mod.filter(id=Myid).update(password=newpassword)
        context = {"info":"修改成功"}
    except:
        context = {"info":"修改失败"}
    return JsonResponse({"msg": context})

@checkLogin
def setpassword(request):
    return render(request,'setpassword.html')


def noUseful(request):
    return render(request,"gotologin.html")


@checkLogin
def manager(request):
    print(request.session.get('login_user')['isManager'])
    try:
        if request.session.get('login_user')['isManager'] == b'\x00':
            return render(request,"notmanager.html")
    except:
        return render(request,"notmanager.html")
    user=[{"id":i.id,"name":i.name,"password":i.password,"isManager":"yes"if i.isManager == b'\x01' else "no","isSuperManager":"yes"if i.isSuperManager == b'\x01' else "no"}for i in UserInfo.objects.all()]
    return render(request,"manager.html",{"user":user})

@checkLogin
@csrf_exempt
def changeUserInfo(request):
    mod = UserInfo.objects
    Myid = request.POST.get('id')
    Myname = request.POST.get('name')
    Mypassword = request.POST.get('password')
    Myis = request.POST.get('isManager')
    Myis = True if Myis == "yes" else False
    print(Myid)
    if request.session.get('login_user')['isSuperManager'] == b'\x00' and UserInfo.objects.get(id=Myid).isManager == b'\x01':
        context = {"info":"修改失败，该用户为管理员而你不是超级管理员"}
        return JsonResponse({"msg": context})
    if UserInfo.objects.get(id=Myid).isSuperManager == b'\x01':
        context = {"info":"修改失败，该用户为超级管理员"}
        return JsonResponse({"msg": context})
    if request.session.get('login_user')['isSuperManager'] == b'\x00' and Myis == True:
        context = {"info":"修改失败，你无权增加管理员"}
        return JsonResponse({"msg": context})
    try:
        mod.filter(id=Myid).update(name=Myname,isManager=Myis,password=Mypassword)
        context = {"info":"修改成功"}
    except:
        context = {"info":"修改失败"}
    return JsonResponse({"msg": context})

