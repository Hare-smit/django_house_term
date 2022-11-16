import requests
import pandas as pd



def dispose_area(area):
    dis = [area,area[:-1], area + "区",area + "镇"]
    return dis

def get_id(area):
    data = pd.read_csv("/Users/huanghanhua/PycharmProjects/analyze_lianjia_Django/funtinos/weather_district_id.csv")
    data_dispose = data.loc[data.district==area,["district_geocode","district"]]
    return list(data_dispose.district_geocode)

def get_area_id(area):
    areas = dispose_area(area)
    try:
        for area in areas:
            id = get_id(area)[0]
            return id
    except:
        pass


def get_weathers(area):
    id = get_area_id(area)
    url = f"https://api.map.baidu.com/weather/v1/?district_id={id}&data_type=all&ak=BVsWXzxHZyXgleHuQWCWmVA5jrBlFTmM"
    data = requests.get(url).json()
    now = data["result"].get("now")
    return now

if __name__=="__main__":
    print(get_weathers("珠海"))
