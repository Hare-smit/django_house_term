import os
import pandas as pd
import pymysql
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import View
from app01 import models
from warehouse.models import Housing
from funtinos.get_weather import *
from app01.static.part.form import Plce
from funtinos.get_location import *
#import subprocess
# Create your views here.



def lianjia_update(request):        #更新数据库--启用scrapy爬虫
    os.system("scrapy crawl lianjia_scrapy")
    # subprocess.Popen('scrapy crawl lianjia_scrapy')
    return HttpResponse('OK')

def main_home(request): #官方主页
    return render(request,"home_page.html")




def print_cl(request,**kwargs):
    context = kwargs if kwargs else {"html":None,"content":None}
    return render(request,context["html"],context["content"])


def plce_edit(request):     #修改地区--更改的是用户地区
    if request.method=="GET":
        form = Plce()
        return render(request,"pl_choice.html",{"form":form,"title":"可视化分析地区"})

    name = request.session.get("info").get("name", "")
    pl_old = models.User.objects.filter(username=name).first()
    form = Plce(data=request.POST, instance=pl_old)
    if form.is_valid():
        form.save()
    return redirect("/show/house/")
#
#
class index_main(View):     #类形式编写的全局分析页面
    # def get(self,request,*args,**kwargs):
    #     return print_cl(request,kwargs["html"],kwargs["content"])
    def get(self,request):
        name = request.session.get("info").get("name","")
        pl = request.user.plce
        weather = get_weathers(pl)
        if pl:
            num = Housing.objects.filter(plce = f"{pl}").count()
            context = {"plce":pl,
                       "title":f"{pl}二手房数据分析平台",
                       "much":num,
                       "weather":weather["text"],
                       "temp":weather["temp"],
                       "img":f"/static/images/weather/{weather['text']}.png",
                       }
            return render(request,"index.html",context)
    def post(self,request):
        return redirect("/list_vi")


@xframe_options_exempt
def cx(request):    #朝向饼图
    #html=f"{self.pl}_cx.html"
    pl = request.user.plce
    return render(request,f"analyze_html/{pl}_cx.html")

@xframe_options_exempt
def zzt(request):       #小区房子平均价
    pl = request.user.plce
    return render(request,f"analyze_html/{pl}_top10.html")

@xframe_options_exempt
def sdt(request):       #面积与总价散点图
    pl = request.user.plce
    return render(request,f"analyze_html/{pl}_sdt.html")

@xframe_options_exempt
def hx(request):    #户型数量玫瑰饼图
    pl = request.user.plce
    return render(request,f"analyze_html/{pl}_hx.html")

@xframe_options_exempt
def ditu(request):  #地图
    pl = request.user.plce
    return render(request,f"analyze_html/{pl}_ditu.html")

def mean(request):  #导航栏
    pl = request.user.plce
    return render(request,"test.html",{"pl":pl})

