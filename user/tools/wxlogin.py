import requests

class Wxlogin:

    _appid = "wx1fe000cec0d68a4e"
    _secret = "7eb9da5267bf3f5f9b9f0da8f34d5c40"
    _grant_type = "authorization_code"

    def get(self,code):
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={self._appid}&secret={self._secret}&js_code={code}&grant_type={self._grant_type}"
        # print(url)
        # print(self._appid,self._secret,self._grant_type)
        try:
            response = requests.get(url)
            data = response.json()
            errcode=data['errcode']
            errmsg=data['errmsg']
            if "session_key" in data and "openid" in data:
                session_id = data["session_key"]
                openid = data["openid"]
                return openid, session_id,None,None,None
            else:
                return None, None,None,errcode,errmsg
        except Exception as e:
            return None, None,e,None,None

