import math


def ditu(pl):
    import pandas as pd
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='hanhua./',
        db='house_term',
        port=3306,
        charset='utf8'
    )

    data = pd.read_sql("select * from warehouse_housing", conn)
    plce_data = data.loc[data.plce==f"{pl}",:]
    #unit_pr = list(plce_data.unit_price)
    pl_data = plce_data["unit_price"]
    plce_data.loc[:,"unit_price"] = pl_data.apply(pd.to_numeric)
    #plce = list(plce_data.plce)[0]
    jq=plce_data.groupby("area")["unit_price"].mean().reset_index()
    area = list(plce_data.area)
    lists1 = [row["area"] for _,row in jq.iterrows()]
    lists2 = [round(row["unit_price"],2)for _,row in jq.iterrows()]
    print(lists1)
    print(lists2)
    max_l = int(max(lists2))
    min_l = int(min(lists2))-1000
    from pyecharts import options as opts
    from pyecharts.charts import Map

    qu_test = "".join(lists1)
    if "区" in qu_test :
        pass
    else:
        lists1 = list(map(lambda x:x+"区",lists1))

    c = (
        Map(init_opts=opts.InitOpts(width="600px",height="500px"))


        .add("",[list(z) for z in zip(lists1,list(map(int,lists2)))], pl)
        .set_global_opts(
            title_opts=opts.TitleOpts(), visualmap_opts=opts.VisualMapOpts(max_=max_l,min_=min_l,
                                                                           is_piecewise=True,
                                                                           textstyle_opts=opts.TextStyleOpts(
                                                                               color="green"
                                                                           )

                                                                           )
        )
        .render(f"../app01/templates/analyze_html/{pl}_ditu.html")
    )

if __name__=="__main__":
    ditu("东莞")