from redis import Redis

class Reds:
    red = Redis(host="127.0.0.1",  # 地址
                 port=6379,   # 端口
                 db=2,   # 数据库
                 password="hanhua./",  # 密码
                 decode_responses=True)  # 是否自动解码

    def red_cheak(self,number):
        if self.red.sismember("ids",number):
            pass
        else:
            pass
    def red_add(self):
        pass