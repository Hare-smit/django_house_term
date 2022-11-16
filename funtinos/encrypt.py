from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
import base64
# 随机
def RSA_create_key():
    #随机
    gen_random = Random.new().read
    # 生成秘钥
    rsakey = RSA.generate(1024,gen_random)
    with open("rsa.public.pem", mode="wb") as f:
        f.write(rsakey.publickey().exportKey())

    with open("rsa.private.pem", mode="wb") as f:
        f.write(rsakey.exportKey())


def RSA_encrypt(data):
    # 加密
    with open("./funtinos/rsa.public.pem", mode="r") as f:
        pk = f.read()
        rsa_pk = RSA.importKey(pk)
        rsa = PKCS1_v1_5.new(rsa_pk)

        result = rsa.encrypt(data.encode("utf-8"))
        # 处理成b64方便传输
        b64_result = base64.b64encode(result).decode("utf-8")
        return b64_result

def RSA_decrypt(data):
    # data = "e/spTGg3roda+iqLK4e2bckNMSgXSNosOVLtWN+ArgaIDgYONPIU9i0rIeTj0ywwXnTIPU734EIoKRFQsLmPpJK4Htte+QlcgRFbuj/hCW1uWiB3mCbyU3ZHKo/Y9UjYMuMfk+H6m8OWHtr+tWjiinMNURQpxbsTiT/1cfifWo4="
    # 解密
    with open("./funtinos/rsa.private.pem", mode="r") as f:
        prikey = f.read()
        rsa_pk = RSA.importKey(prikey)
        rsa = PKCS1_v1_5.new(rsa_pk)
        result = rsa.decrypt(base64.b64decode(data), None)
        return result.decode("utf-8")


if __name__ == "__main__":
    RSA_create_key()