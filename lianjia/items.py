# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from warehouse.models import Housing
from scrapy_djangoitem import DjangoItem

class LianjiaItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Housing

    '''
    area = scrapy.Field()
    title = scrapy.Field()
    community = scrapy.Field()
    position = scrapy.Field()
    tag = scrapy.Field()
    re_price = scrapy.Field()
    unit_price = scrapy.Field()
    housetype = scrapy.Field()
    housesize = scrapy.Field()
    direction = scrapy.Field()
    fitment = scrapy.Field()
    plce = scrapy.Field()
    '''
