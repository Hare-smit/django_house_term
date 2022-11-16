from app01 import models
from django import forms
from warehouse.models import Housing
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.static.part.bootstrap import BootStrapModelForm
from app01.static.part.encrypt_md5 import md5
from funtinos.encrypt import RSA_encrypt,RSA_decrypt
from django.contrib.auth import get_user_model
#
class Admin_add(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",widget=forms.PasswordInput(render_value=True))

    class Meta:
        model=models.User
        fields = ["email","username","password","confirm_password","plce"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm
#
class Admin_check(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",widget=forms.PasswordInput(render_value=True))

    class Meta:
        model=models.User
        fields = ["password","confirm_password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }


    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

class Login(BootStrapModelForm):
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True,
    )
    class Meta:
        model =models.User
        fields = ["username","code","password"]
        widgets={
            "password":forms.PasswordInput
        }

    # def clean_password(self):
    #     pwd = RSA_decrypt(self.cleaned_data.get("password"))
    #     print(pwd)
    #     return pwd

#
#
class Plce(BootStrapModelForm):
    class Meta:
        model=models.User
        fields=["plce"]

#
# class House_type(BootStrapModelForm):
#
#     class Meta:
#         model= Housing
#         fields = "__all__"
#


# class Order(BootStrapModelForm):
#     class Meta:
#         model = models.Order
#         fields = "__all__"
#         exclude=["order_num","admin"]
#
# class FileModelForm(BootStrapModelForm):
#     bootstrap_exclude_fields = ["img"]
#
#     class Meta:
#         model = models.City
#         fields = "__all__"
