from django.db import models

# Create your models here.
class Housing(models.Model):
    area = models.CharField(verbose_name="区",max_length=32)
    title = models.CharField(verbose_name="标题",max_length=256)
    community = models.CharField(verbose_name="小区",max_length=64)
    position = models.CharField(verbose_name="地段",max_length=32)
    tag = models.TextField(verbose_name="标签")
    re_price = models.CharField(verbose_name="总价",max_length=32)
    unit_price = models.CharField(verbose_name="平方价",max_length=32)
    housetype = models.CharField(verbose_name="房型",max_length=64)
    housesize = models.CharField(verbose_name="面积",max_length=32)
    direction = models.CharField(verbose_name="朝向",max_length=32)
    fitment = models.CharField(max_length=32,verbose_name="装修格局")
    plce = models.CharField(max_length=32,verbose_name="地区")
    master_map = models.CharField(max_length=255,verbose_name="图片")
    house_id = models.CharField(max_length = 32, verbose_name = "id号",default="1")
