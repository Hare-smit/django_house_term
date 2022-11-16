from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from app01 import models
from django.shortcuts import render,redirect,HttpResponse
from app01.static.part.code import check_code
from io import BytesIO
from app01.static.part.form import Login
from funtinos.encrypt import RSA_encrypt,RSA_decrypt
from django.contrib.sessions.models import Session

def session_del(name):
    sessionArr = Session.objects.all()
    for item in sessionArr:
        # 将用户信息解密
        item_se_data = item.get_decoded()
        print(item_se_data)
        # logout_tickets 是我们删选要退出的用户的信息，这个要存到了session里面
        # if item_se_data.get("", "") == name:
        #     # 拿到需下线用户的sessionid，通过id删除
        #     item_se_id = item.session_key
        #     Session.objects.get(pk=item_se_id).delete()






def logins(request):
    with open("./funtinos/rsa.public.pem", mode="r") as f:
        pub_key = f.read()      #公钥
    if request.method=="GET":
        form = Login()
        return render(request,"login.html",{"form":form,"pub_key":pub_key}) #get请求进入登录页
    # print(pub_key)
    form = Login(data=request.POST)     #获取post请求中的信息
    if form.is_valid():
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code","")#可能因为过时没有了所以获取时候为none这里设置让他为""
        if code.upper() != user_input_code.upper():
            form.add_error("code","验证码输入不正确")
            return render(request, "login.html", {"form": form,"pub_key":pub_key})
        username = request.POST["username"]
        password = RSA_decrypt(request.POST["password"])
        print(username,password)
        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            form.add_error("password","用户名或者密码不正确")
            return render(request, "login.html", {"form": form,"pub_key":pub_key})
        login(request,user)
        pl = user.plce
        request.session["info"] = {"id":user.id,"name":user.username,"plce":pl}
        #session设置了保留7天
        request.session.set_expiry(60*60*24*7)
        return redirect("/main/home/")
    return render(request, "login.html", {"form": form,"pub_key":pub_key})

def logouts(request):
    logout(request)
    return redirect("/login/")

def image_code(request):
    #调用pillow函数生成图片
    img,code_string = check_code()

    #写入session中（以便后续获取验证码再进行校验）
    request.session["image_code"]=code_string
    #给session 设置60s超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream,"png")
    #stream.getvalue()
    return HttpResponse(stream.getvalue())

