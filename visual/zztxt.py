def zzt(pl):
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
    plce_data = data.loc[data.plce == f"{pl}", :].set_index("community")
    plce_data.loc[:,"unit_price"] = plce_data["unit_price"].apply(pd.to_numeric)
    datas = plce_data.groupby("community")["area",].count().sort_values(by="area",ascending=False).head(10).reset_index()
    dat_comunity = [row["community"] for _, row in datas.iterrows()]
    dat_count = list(datas.area)
    dats = plce_data.loc[dat_comunity,:].groupby("community",sort =False).mean().reset_index()
    unitprice = [round(row["unit_price"],2) for _, row in dats.iterrows()]
    #data_mean = datas.groupby("comunity")["unitPrice"].mean().reset_index()
    from pyecharts import options as opts
    from pyecharts.charts import Bar, Line

    line = Line().add_xaxis(dat_comunity).\
        add_yaxis("小区每平方米均价", unitprice, yaxis_index=1,
                  linestyle_opts=opts.LineStyleOpts(color="#7fff00"),
                  label_opts=opts.LabelOpts(color="green"))
    bar = (
        Bar(init_opts=opts.InitOpts(width="410px",height="300px"))
        .add_xaxis(dat_comunity)
        .add_yaxis("套数", dat_count,color="#fadb71",)
        .extend_axis(
            yaxis=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} 元"),
                interval=8000,
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="green"))
            )
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(),
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts("green")),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15),
                                     axisline_opts=opts.AxisLineOpts(
                                         linestyle_opts=opts.LineStyleOpts(color="green"))),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 套"),
                                     interval=20,
                                     max_=60,
                                     axisline_opts=opts.AxisLineOpts(
                                         linestyle_opts=opts.LineStyleOpts(color="green")
                                     )),
        )
    )

    #line = Line().add_xaxis(dat_comunity).add_yaxis("小区每平方米均价", unitprice, yaxis_index=1)
    bar.overlap(line)

    bar.render(f"../app01/templates/analyze_html/{pl}_top10.html")

if __name__=="__main__":
    zzt("广州")