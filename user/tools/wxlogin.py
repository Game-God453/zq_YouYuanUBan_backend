import requests

class Wxlogin:

    _appid = ""
    _secret = ""
    _grant_type = "authorization_code"

    def get(self,code):
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={self._appid}&secret={self._secret}&js_code={code}&grant_type={self._grant_type}"
        try:
            response = requests.get(url)
            data = response.json()
            session_id = data["session_key"]
            openid = data["openid"]
            if not openid and not session_id:
                return openid,session_id
        except Exception as e:
            print(e)
            return None

