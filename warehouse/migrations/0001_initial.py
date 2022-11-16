# Generated by Django 4.1.3 on 2022-11-15 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Housing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=32, verbose_name='区')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('community', models.CharField(max_length=64, verbose_name='小区')),
                ('position', models.CharField(max_length=32, verbose_name='地段')),
                ('tag', models.TextField(verbose_name='标签')),
                ('re_price', models.CharField(max_length=32, verbose_name='总价')),
                ('unit_price', models.CharField(max_length=32, verbose_name='平方价')),
                ('housetype', models.CharField(max_length=64, verbose_name='房型')),
                ('housesize', models.CharField(max_length=32, verbose_name='面积')),
                ('direction', models.CharField(max_length=32, verbose_name='朝向')),
                ('fitment', models.CharField(max_length=32, verbose_name='装修格局')),
                ('plce', models.CharField(max_length=32, verbose_name='地区')),
                ('master_map', models.CharField(max_length=255, verbose_name='图片')),
                ('house_id', models.CharField(default='1', max_length=32, verbose_name='id号')),
            ],
        ),
    ]
