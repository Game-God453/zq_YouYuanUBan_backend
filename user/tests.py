import random
import string

from user.tools.JWTtoken import JWTToken


def generate_random_string(length=6):
    # 定义字符池，包含大小写字母和数字
    characters = string.ascii_letters + string.digits
    # 使用random.choices随机选择字符
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


openid = "i7FDc5"
session_key = generate_random_string(12)
# 如果当前用户已处于登录状态，则删除之前的token，重新登录


token = JWTToken(openid, session_key).encode()

print(token)
