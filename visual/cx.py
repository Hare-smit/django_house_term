def cx(pl):
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
    data = pd.read_sql("select * from warehouse_housing",conn)
    plce_data = data.loc[data.plce ==f"{pl}",:]
    data_direction = plce_data.groupby("direction")["area"].count().sort_values(ascending=False).head(10).reset_index()
    # print(data_direction)


    # from pyecharts import options as opts
    # from pyecharts.charts import Pie

    dir=[row["direction"] for _, row in data_direction.iterrows()]
    num=[row["area"] for _, row in data_direction.iterrows()]

    import pyecharts.options as opts
    from pyecharts.charts import Pie


    (
        Pie(init_opts=opts.InitOpts(width="350px", height="300px"))
        .add(
            series_name="朝向:",
            data_pair=[list(z) for z in zip(dir, num)],
            radius=["30%", "60%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left="right", orient="horizontal",
                                                     textstyle_opts=opts.
                                                     TextStyleOpts(color="green")))
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            # label_opts=opts.LabelOpts(formatter="{b}: {c}")
        )
        .render(f"../app01/templates/analyze_html/{pl}_cx.html")
    )


if __name__=="__main__":
    cx()






