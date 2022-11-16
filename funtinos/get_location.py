import requests

def geocoding(address,area):        #获取经纬度geocoding("和平里五区 - 和平里","北京")
    """
    address convert lat and lng
    :param address: address
    :param currentkey: AK
    :return: places_ll
    """
    places_ll=[]
    url = 'http://api.map.baidu.com/geocoding/v3/?'
    params = {
        "address": address,
        "city": area,
        "output": 'json',
        "ak": 'w5o5Bvg1NwQV53gTzOfAPqrKKqPUlMXZ',
    }
    response = requests.get(url, params=params)
    answer = response.json()
    if answer['status'] == 0:
        tmpList = answer['result']
        coordString = tmpList['location']
        coordList = [coordString['lng'], coordString['lat']]
        places_ll.append([address, float(coordList[0]), float(coordList[1])])
        return [address, float(coordList[0]), float(coordList[1])]
    else:
        return -1



def surrounding(location,query,tag):        #获取周边环境surrounding(location, "交通设施", "地铁站")
    dining_ll = []
    url = "https://api.map.baidu.com/place/v2/search?"
    params = {
        "query": query,
        "tag":tag,
        "location":f"{location[2]},{location[1]}",
        "output":"json",
        "radius":"1000",
        "ak": 'w5o5Bvg1NwQV53gTzOfAPqrKKqPUlMXZ',
    }
    response = requests.get(url, params=params)
    answer = response.json()
    print(answer)
    if answer['status'] == 0:
        #print(answer)
        dining = answer["results"]
        for din in dining:
            dining_ll.append((din["name"],din["address"]))
        print(dining_ll)
        return dining_ll

    else:
        return -1



#X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]#所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')#这里获得代理ip
    return ip

def get_ip_location(ip):
    url = f"https://api.map.baidu.com/location/ip?ak=w5o5Bvg1NwQV53gTzOfAPqrKKqPUlMXZ&ip={ip}&coor=bd09ll"
    response = requests.get(url)
    answer = response.json()
    print(answer)


if __name__=="__main__":
    location =  geocoding("和平里五区 - 和平里","北京")
    print(location)
    # dining = surrounding(location, "美食", "中餐")
    # traffic = surrounding(location, "交通设施", "地铁站")
    # traffic1 = surrounding(location, "交通设施", "公交车站")
    # traffic2 = surrounding(location, "交通设施", "充电站")
    # store = surrounding(location, "购物", "购物中心")
    ip="120.235.224.155"
    get_ip_location(ip)
    surrounding(location, "交通设施", "地铁站")
    surrounding(location, "交通设施", "充电站")