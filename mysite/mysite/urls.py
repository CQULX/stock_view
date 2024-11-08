"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,re_path
from stock_view import views

urlpatterns = [
    path('rankByMap/',views.rankByMap),
    path('rankByTrade/', views.rankByTrade),
    path('Allrank/',views.Allrank),
    path('',views.login),
    path('index/', views.index),
    path('login/',views.login),
    path('user/list/',views.user_list),
    path('user/add/',views.user_add),
    path('register/',views.register),
    path('test/',views.test),
    path('stock_search/',views.stock_search),
    path('trade_search/',views.trade_search),
    path('starbox/',views.starbox),
    path('company_search/',views.company_search),
    path('company_search/<str:id>/', views.company_search_detail),
    path('trade_search/<str:id>/', views.trade_search_detail),
    path('stock_search/<str:id>/',views.stock_search_detail),
    path('starbox/',views.starbox),
    path('userSettings/', views.Usersettings),
    path('UserSet/', views.UserInfoSet),
    path('deleteProductByIdList/',views.deleteProductByIdList),
    path('changepassword/',views.changeMyPassword),
    path('setpassword/',views.setpassword),
    path('gotologin/',views.noUseful),
    path('manager/',views.manager),
    path('notmanager/',views.noUseful),
    path('changeUserInfo/',views.changeUserInfo),
    re_path(r'^trade/(.+)/$', views.get_trade),
    path('addProduct/',views.addProduct),
    path('deleteProduct/',views.deleteProduct),
    path('pre/',views.predictStock),
]
