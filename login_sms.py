import httpx

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 30; ) Okhttp/4.11.0"
}


def send_sms(phone: str) -> bool:
    """
    发送短信验证码

    :param phone: 鹰角网络账号 手机号
    :return: True为发送成功
    """
    resp = httpx.post("https://as.hypergryph.com/general/v1/send_phone_code", headers=headers,
                      json={"phone": phone, "type": 2})
    if resp.status_code != 200:
        print(f"Send SMS Error: \n{resp.text}")
        exit(0)
    data = resp.json()
    if data["status"] != 0:
        print(f"Send SMS Error: \n{resp.text}")
        exit(0)
    return True



def login_sms(phone: str, code: str) -> str:
    """
    使用短信验证码登录鹰角网络账号

    :param phone: 鹰角网络账号 手机号
    :param code: 登入验证码
    :return: 登入后的token data.token
    """
    resp = httpx.post("https://as.hypergryph.com/user/auth/v2/token_by_phone_code", headers=headers,
                      json={"phone": phone, "code": code})
    if resp.status_code != 200:
        print(f"Login Error: \n{resp.text}")
        exit(0)
    data = resp.json()
    if data["status"] != 0:
        if data["status"] == 101:
            print("手机号验证码错误! ")
        print(f"Login Error: \n{resp.text}")
        exit(0)
    return data["data"]["token"]


if __name__ == '__main__':
    user_phone = "12345678901"
    if not send_sms(user_phone):
        print("验证码发送失败")
        exit(0)
    user_code = input("请输入短信验证码")
    try:
        int(user_code)
    except ValueError:
        print("你输入的并不是数字")
        exit(0)
    token = login_sms(user_phone, user_code)
    if token:
        print(f"鹰角网络账号登入成功，获取到的Token为: {token}")
