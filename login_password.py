import httpx

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 30; ) Okhttp/4.11.0"
}


def login_password(phone: str, password: str) -> str:
    """
    使用账号密码登录鹰角网络账号

    :param phone: 鹰角网络账号手偶家
    :param password: 鹰角网络账号密码
    :return: 登入后的token data.token
    """
    resp = httpx.post("https://as.hypergryph.com/user/auth/v1/token_by_phone_password", headers=headers,
                      json={"phone": phone, "password": password})
    if resp.status_code != 200:
        print(f"Login Error: \n{resp.text}")
        exit(0)
    data = resp.json()
    if data["status"] != 0:
        if data["status"] == 100:
            print("账号密码错误! ")
        print(f"Login Error: \n{resp.text}")
        exit(0)
    return data["data"]["token"]


if __name__ == '__main__':
    token = login_password("12345678901", "abcdefg")
    if token:
        print(f"鹰角网络账号登入成功，获取到的Token为: {token}")
