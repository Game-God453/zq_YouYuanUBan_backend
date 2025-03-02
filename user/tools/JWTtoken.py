import datetime

import jwt
from jwt import ExpiredSignatureError
from django.conf import settings


class JWTToken:
    _secretKey = "your_secret_key"

    def __init__(self,openid,session_key):
        exp = datetime.datetime.now() + datetime.timedelta(seconds=getattr(settings, "TOKEN_TTL", 60 )) #默认1分钟

        # print(f"登录发放的token过期时间：{exp}\n现在的时间：{datetime.datetime.now()}")

        self.payload = {'openid': openid, "session_key": session_key, "login_time": datetime.datetime.now().isoformat(),
                        'exp': exp.timestamp()}

    def encode(self):
        token = jwt.encode(self.payload, self._secretKey, algorithm="HS256")
        return token

    @classmethod
    def decode(cls,token):

        try:
            # 解码并验证 Token
            # algorithms 参数必须与生成 Token 时使用的算法一致
            decoded_payload = jwt.decode(token, cls._secretKey, algorithms=["HS256"],verify_expiration=True)

            # print(f"登录发放的token过期时间：{decoded_payload["exp"]}\n现在的时间：{datetime.datetime.now()}")

            return decoded_payload, "登录验证成功"
        except ExpiredSignatureError:
            print("Token 已过期！")
            return None, "登录已过期！"

        except jwt.InvalidTokenError:
            print("Token 无效！")
            return None, "Token 无效！"

        except Exception as e:
            print(f"其他错误：{e}")
            return None, e

