# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymysql
# useful for handling different item types with a single interface
from warehouse import models
from visual import visual_main
from funtinos import data_up
from funtinos.redis_check_up import Reds

class LianjiaPipeline(object):
    tt = [] #装载每次插入的数据
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="hanhua./",
                                    database="house_term", charset='utf8')
        self.cursor = self.conn.cursor()    #定义游标
        self.red = Reds.red     #连接redis

    def open_spider(self, spider):
        #增量爬虫注释掉
        # self.cursor.execute("truncate table warehouse_housing")#_update;")  #清空数据库
        # self.conn.commit()  #执行
        print("redis开启")
        pass




    def close_spider(self, spider):
        print("closing spider,last commit", len(self.tt))
        self.bulk_insert_to_mysql(self.tt,"warehouse_housing")#_update")
        self.conn.commit()
        time.sleep(1)
        visual_main.make_main()
        print("html更新完成")
        if self.red:
            self.red.close()
            print("redis已关闭")
        """
        #查看获取爬去数据是否足够
        # len_s = models.Housing_update.objects.count()
        # time.sleep(1)
        # if len_s>1000:
        #     print("符合标准")
        #     time.sleep(1)
        #     data_up.update_datebases()
        #     
        # time.sleep(1)
        # visual_main.make_main()
        # print("html更新完成")
        #
        #     self.cursor.execute("truncate table warehouse_housing;")  # 清空数据库
        #     self.conn.commit()
        #     self.bulk_insert_to_mysql(relist1,"warehouse_housing")
        #     #print("爬取入库完成")
        # self.cursor.close()
        # self.conn.close()
        """


    #插入函数
    def bulk_insert_to_mysql(self, list,db):   #插入函数
        try:
            print("the length of the data-------", len(self.tt))
            sql = f"insert into {db}(area,title,community,position,tag,re_price,unit_price,housetype,housesize,direction,fitment,plce,master_map,house_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            self.cursor.executemany(sql, list)  #插入数据   插入多用executemany，少用exectue
            self.conn.commit()
        except:
            self.conn.rollback()



    def process_item(self, item, spider):
        # print(item)
        area = item["area"]
        title = item["title"]
        community = item["community"]
        position = item["position"]
        tag = item["tag"]
        re_price = round(float(item['re_price']),2)

        unit = item["unit_price"]
        units = unit.replace(",","")[:-3]
        unit_price = round(float(units),2)

        housetype = item["housetype"]
        housesize = round(float(item["housesize"]),2)
        direction = item["direction"]
        fitment = item["fitment"]
        plce = item["plce"]
        master_map = item["master_map"]
        house_id = item["house_id"]
        if self.red.sismember("ids", house_id):
            print("已存在")
        else:
            self.red.sadd("ids", house_id)
            self.tt.append((area,title,community,position,tag,re_price,unit_price,housetype,housesize,direction,fitment,plce,master_map,house_id))
            print(f"新增:{house_id}")
            if len(self.tt) == 88:
                self.bulk_insert_to_mysql(self.tt,"warehouse_housing")#_update")
                # 清空缓冲区
                del self.tt[:]
        # sql = "insert into taobao(title,price,place,sell,store) values (%s,%s,%s,%s,%s)"
        # self.curser.executemany(sql,self.tt)
        return item









    #
    # def process_item(self, item, spider):
    #     print('打开了数据库')
    #     print(item)
    #     # item.save()
    #     print('关闭了数据库')
    #     return item
