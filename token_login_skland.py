import httpx

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 30; ) Okhttp/4.11.0"
}


def get_login_code(token: str) -> str:
    """
    使用短信验证码/用户密码登入获取到的token获取skland登入需要的code

    :param token: 短信验证码/用户密码登入获取到的token
    :return: skland登入需要的code
    """
    resp = httpx.post("https://as.hypergryph.com/user/oauth2/v2/grant", headers=headers,
                      json={"token": token, "appCode": "4ca99fa6b56cc2ba", "type": 0})
    if resp.status_code != 200:
        print(f"Get code Error: \n{resp.text}")
        exit(0)
    data = resp.json()
    if data["status"] != 0:
        print(f"Get code Error: \n{resp.text}")
        exit(0)
    return data["data"]["code"]


def code_get_cred(code: str) -> str:
    """
    使用 get_login_code 获取到的code来获取到skland身份验证需要的cred

    :param code: get_login_code 获取到的code
    :return: skland的 cred
    """
    resp = httpx.post("https://zonai.skland.com/api/v1/user/auth/generate_cred_by_code", headers=headers,
                      json={"kind": 1, "code": code})
    if resp.status_code != 200:
        print(f"Get cred Error: \n{resp.text}")
        exit(0)
    data = resp.json()
    if data["status"] != 0:
        print(f"Get cred Error: \n{resp.text}")
        exit(0)
    return data["data"]["cred"]


if __name__ == '__main__':
    token = input("请输入短信登入/密码登入获取到的token")
    code = get_login_code(token)
    cred = code_get_cred(code)
    print(f"已获取到cred: {cred}\n软件调用请在header头带上进行使用\n cred: {cred}")
