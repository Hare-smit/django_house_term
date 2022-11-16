import pymysql

def update_datebases():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="hanhua./",
                                        database="lianjia", charset='utf8')

    cursor = conn.cursor()
    # 更新爬取的数据，进入呈现的数据库


    def select(sql):  # 获取函数，不用此方法游标缘故获取内容会有问题
        cursor.execute(sql)
        relist = cursor.fetchall()
        return relist

    sql1 = "select * from warehouse_housing_update;"
    relist1 = select(sql1)  # 获取到内容
    print(relist1)


    cursor.execute("truncate table warehouse_housing;")  # 清空数据库
    conn.commit()
    # try:

    sql = f"insert into warehouse_housing(id,area,title,community,position,tag,re_price,unit_price,housetype,housesize,direction,fitment,plce,master_map) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.executemany(sql, relist1)  # 插入数据   插入多用executemany，
    conn.commit()
    conn.close()
# except:
#     conn.rollback()
# print("更新入库完成")
if __name__=="__main__":
    update_datebases()