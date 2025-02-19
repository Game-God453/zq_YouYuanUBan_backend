import datetime

import jwt
from jwt import ExpiredSignatureError
from django.conf import settings


class JWTToken:
    _secretKey = "your_secret_key"

    def __init__(self,openid,session_key):
        exp = datetime.datetime.now() + datetime.timedelta(seconds=getattr(settings, "TOKEN_TTL", 60 )) #默认1分钟

        self.payload = {'openid': openid, "session_key": session_key, "login_time": datetime.datetime.now().isoformat(),'exp': exp}

    def encode(self):
        token = jwt.encode(self.payload, self._secretKey, algorithm="HS256")
        return token

    @classmethod
    def decode(cls,token):

        try:
            # 解码并验证 Token
            # algorithms 参数必须与生成 Token 时使用的算法一致
            decoded_payload = jwt.decode(token, cls._secretKey, algorithms=["HS256"])
            return decoded_payload
        except ExpiredSignatureError:
            print("Token 已过期！")
            return None

        except jwt.InvalidTokenError:
            print("Token 无效！")
            return None

        except Exception as e:
            print(f"其他错误：{e}")
            return None

