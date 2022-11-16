"""django_house_term URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import requests
from django.contrib import admin
from django.urls import path, re_path
from app01.views import index,account_login,admins,show_house
from app01 import models

urlpatterns = [
#功能页
    path('admin/', admin.site.urls),#admin，Django管理页面
    path("main/home/", index.main_home, name="home"),   #主页
    path('lianjia/update/', index.lianjia_update, name="update_climb"), #爬虫更新

#分析视图
    re_path("list_vi/",index.index_main.as_view(),name="list"),
    path("edit/",index.plce_edit,name="pl_edit"),
    path("cx/", index.cx, name="cx"),
    path("zzt/", index.zzt, name="top10"),
    path("sdt/", index.sdt, name="sdt"),
    path("hx/", index.hx, name="hx"),
    path("dt/", index.ditu, name="dt"),
    path("menu/",index.mean,name="menu"),
#登陆页面
    path("login/", account_login.logins, name="login"),
    path("logout/", account_login.logouts, name="logout"),
    path("image/make/", account_login.image_code, name="image"),
#添加用户
    path("admins/add/", admins.admin_add, name="admin_add"),
    path("admins/reset/", admins.admin_reset, name = "reset"),
# 内容展示
    path("show/house/", show_house.house, name="show"),
    path("show/<int:nid>/info/", show_house.house_info)
]
