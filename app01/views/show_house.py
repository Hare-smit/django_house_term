from concurrent.futures.thread import ThreadPoolExecutor

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django import forms
from django.db.models import Q
from funtinos.get_weather import *
from warehouse import models
from app01.static.part.pagination import Pagination
from funtinos.get_location import *
from threading import Thread,Condition,current_thread
from app01.models import User


def house(request):     #房子总览
    search_data = request.GET.get("q","")
    name = request.user.username
    pl = User.objects.filter(username=name).first().plce
    if search_data:
        queryset = models.Housing.objects.filter(Q(title__contains=search_data) | Q(community__contains=search_data) | Q(community__contains=search_data) | Q(community__contains=search_data) | Q(position__contains=search_data) | Q(tag__contains=search_data))
    else:
    #form = models.Housing.objects.all()
        queryset = models.Housing.objects.filter(plce=pl)
    page_object = Pagination(request,queryset,page_size=8,plus=2,)
    pl = request.user.plce
    weather = get_weathers(pl)
    wea = weather["text"]
    context = {
        "querset":page_object.page_queryset,
        "page_string":page_object.html(),
        "search_data":search_data,
        "title":"新建管理员",
        "weather":weather,
        "pl":pl
    }
    return render(request,"house_type.html",context)


def house_info(request,nid):        #房子详细内容
    house_id = models.Housing.objects.filter(id = nid).first()
    address = house_id.community+house_id.position
    location = geocoding(address,house_id.area)
    location_list = ",".join(map(str,location[1:]))
    dining = surrounding(location,"美食","中餐")
    traffic = surrounding(location,"交通设施","地铁站")
    traffic2 = surrounding(location,"交通设施","充电站")
    store = surrounding(location,"购物","购物中心")

    # with ThreadPoolExecutor(max_workers=8) as pool:
    #     dining = pool.submit(surrounding,(location,"美食","中餐"))
    #     traffic = pool.submit(surrounding,(location,"交通设施","地铁站"))
    #     traffic1 = pool.submit(surrounding,(location,"交通设施","公交车站"))
    #     traffic2 = pool.submit(surrounding,(location,"交通设施","充电站"))
    #     store = pool.submit(surrounding,(location,"购物","购物中心"))


    context={
        "item":house_id,
        "dining":dining,
        "traffic":traffic,
        # "tra1":traffic1,
        "tra2":traffic2,
        "store":store,
        "location" : location_list,
        #"pl": pl,

    }
    return render(request,"house_info.html",context)

