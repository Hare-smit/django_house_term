import random
import re
import time

import scrapy
from scrapy import Request,Selector
from scrapy.http import HtmlResponse
from lianjia.selen_req import SeleniumRequest
from lianjia.items import LianjiaItem

class LianjiaScrapySpider(scrapy.Spider):
    name = 'lianjia_scrapy'
    allowed_domains = ['lianjia.com']
    #start_urls = [f'https://bj.lianjia.com/ershoufang//']
#传入城市链接进入访问，为了获取area内容
    def start_requests(self):
        placs=["bj","gz","dg","hui","jiangmen","qy","sz","zh","zhanjiang","zs","fs",]
        for plac in placs:
            url = f'https://{plac}.lianjia.com/ershoufang/'
            yield Request(url=url)


#获取area，将信息传入链接从而访问
    def parse(self, response:HtmlResponse,**kwargs):
        # lianjia = LianjiaItem()
        sel = Selector(response)
        areas = sel.xpath('//div[@data-role="ershoufang"]')
        area = areas.xpath('.//a/text()').extract()
        area_href = areas.xpath('.//a/@href').extract()
        area_double = zip(area,area_href)
        for href in area_double:
            lianjia = LianjiaItem()
            href_dis = href[1].split('/')[2]
            lianjia['area'] = href[0]
            url = response.urljoin(href_dis+'/')
            check = sel.css('#content > div.leftContent > ul > li')
            if check ==[]:
                continue
            yield Request(url=url,callback=self.page_house,cb_kwargs= dict(lianjia,main_url=response.url+href_dis+'/',page_on=1))  #获取到当前区域的链接，进入区域继续获取

    def page_house(self,response:HtmlResponse,**kwargs):
        lianjia=kwargs
        main_url = kwargs['main_url']
        sel = Selector(response)
        All = sel.css('#content > div.leftContent > ul > li')
        for nu in range(7,10):
            plce = sel.xpath(f'//*[@id="content"]/div[1]/div[{nu}]/div[1]/a[1]/text()').extract_first()
            if plce != None:
                break
        # print(plce)
        lianjia['plce'] = plce.replace('房产网','')
#'//div[@comp-module="page"]/a[@class="on"]/text()'
        #page_on = sel.xpath('//div[@comp-module="page"]/a[@class="on"]/text()').extract_first()
        for chunk in All:
            try:
                lianjia['title'] = chunk.xpath('.//div[@class="title"]/a/text()').extract_first()
                re_ = re.compile("ershoufang/(?P<id>.*?).html",re.S)
                id = chunk.xpath('.//div[@class="title"]/a/@href').extract_first()
                lianjia["house_id"] = re_.search(id).group("id")
                try:
                    community,position = chunk.xpath('.//div[@class="positionInfo"]/a/text()').extract()
                except:
                    community ,position = chunk.xpath('.//div[@class="positionInfo"]/a/text()').extract_first(),None

                lianjia['community'], lianjia['position']= community,position

                tag = chunk.xpath('.//div[@class="tag"]/span/text()').extract()
                lianjia['tag'] = "  |  ".join(tag)

                lianjia['re_price'] = chunk.xpath('.//div[@class="priceInfo"]/div/span/text()').extract_first()

                lianjia['unit_price'] = chunk.xpath('.//div[@class="priceInfo"]//div[@class="unitPrice"]/span/text()').extract_first()

                houseticon = chunk.css('div.info.clear > div.address > div.houseInfo::text').extract_first()
                # print(houseticon)

                lianjia['housetype'] = houseticon.split('|')[0]

                lianjia['housesize'] = houseticon.split('|')[1].replace('平米','')

                lianjia['direction'] = houseticon.split('|')[2]

                lianjia['fitment'] = houseticon.split('|')[3]

                lianjia["master_map"] = chunk.xpath(".//img[@class='lj-lazy']/@data-original").extract_first()
            except:
                continue

            #print(lianjia)
            yield lianjia

        if kwargs['page_on'] < 2:
            kwargs['page_on'] += 1
            print(f'爬取{lianjia["area"]}第{kwargs["page_on"]}页')
            next_url = main_url+f'pg{kwargs["page_on"]}/'
            # time.sleep(random.randint(1,2))
            yield Request(url=next_url,callback=self.page_house,cb_kwargs= dict(lianjia))





        # area = scrapy.Field()
        # title = scrapy.Field()
        # community = scrapy.Field()
        # position = scrapy.Field()
        # tag = scrapy.Field()
        # re_price = scrapy.Field()
        # unit_price = scrapy.Field()
        # hoursetype = scrapy.Field()
        # hoursesize = scrapy.Field()
        # direction = scrapy.Field()
        # fitment = scrapy.Field()
        # plce = scrapy.Field()

