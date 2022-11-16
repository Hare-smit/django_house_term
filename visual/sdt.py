
def sdts(pl):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Scatter
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
    plce_data = data.loc[data.plce == f"{pl}", :]
    sam = plce_data[["housesize","re_price"]]
    houres = list(map(float,[row["housesize"] for _ ,row in sam.iterrows()]))
    to_price = list(map(float,[row["re_price"] for _ ,row in sam.iterrows()]))
    #print(data["houressize"])
    print(houres)
    print(to_price)
    c = (

        Scatter(init_opts=opts.InitOpts(width="450px",height="280px"))
        .add_xaxis(houres)
        .add_yaxis("", to_price)
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=1000,
                                              textstyle_opts=opts.TextStyleOpts(color="green"),orient="horizontal"
                                              ),
            xaxis_opts=opts.AxisOpts(max_=400,
                                     axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="green"))),
            yaxis_opts=opts.AxisOpts(max_=5000,interval=1000,
                                     axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="green"))),


        )
        .render(f"../app01/templates/analyze_html/{pl}_sdt.html")
    )
if __name__=="__main__":
    sdts("深圳")