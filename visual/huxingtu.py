def huxingtu(pl):
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
    plce_data = data.loc[data.plce == f"{pl}", :]
    jq=plce_data.groupby("housetype")["area"].count().reset_index()

    jq=jq.sort_values(by="area",ascending=False)[0:5]
    lists1 = [row["housetype"] for _,row in jq.iterrows()]
    lists2 = [row["area"] for _,row in jq.iterrows()]


    import pyecharts.options as opts
    from pyecharts.charts import Pie

    """
    Gallery 使用 pyecharts 1.1.0
    参考地址: https://echarts.apache.org/examples/editor.html?c=pie-doughnut
    
    目前无法实现的功能:
    
    1、迷之颜色映射的问题
    """

    x_data = lists1
    y_data = lists2
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])

    (
        Pie(init_opts=opts.InitOpts(width="500px", height="300px"))
        .add(
            series_name="户型",
            data_pair=data_pair,
            rosetype="radius",
            radius="55%",
            center=["40%", "40%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="",
                pos_left="center",
                pos_top="20",
                title_textstyle_opts=opts.TextStyleOpts(color="while"),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(color="green"),
        )
        .render(f"../app01/templates/analyze_html/{pl}_hx.html")
    )

if __name__=="__main__":
    huxingtu()