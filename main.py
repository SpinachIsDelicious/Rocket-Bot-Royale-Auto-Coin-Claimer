from asyncio import run
from curl_cffi import AsyncSession
from time import sleep

AUTH_URL = "https://dev-nakama.winterpixel.io/v2/account/authenticate/email?create=false&"
URL = "https://dev-nakama.winterpixel.io/v2/rpc/collect_timed_bonus"
SERVER_KEY = "OTAyaXViZGFmOWgyZTlocXBldzBmYjlhZWIzOTo="
AuthData:list[str] = list()
# index 0, token
# index 1, refresh token

# optionally put email & pass in, or wait for script prompt
email = ""
password = ""

if not email or not password:
    email = input("Email: ")
    password = input("Password: ")
    
data = {"email":email,"password":password,"vars":{"client_version":"81"}}

async def authenticate():
    payload = {
        "email": email,
        "password": password,
        "vars": {"client_version": "81"},
    }

    async with AsyncSession(allow_redirects=True, headers={"Authorization": f"Basic {SERVER_KEY}","accept": "application/json","content-type": "application/json","user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ""(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"),}) as s:
        # 1) Authenticate (HTTP server key required)
        r = await s.post(AUTH_URL, json=payload, timeout=30)
        print("Auth Status:", r.status_code)
        print("Auth Body:", r.text)

        AuthData.append(r.json()["token"]) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
        AuthData.append(r.json()["refresh_token"]) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

async def claim_coins():
    async with AsyncSession(allow_redirects=True, headers={"Authorization": f"Bearer {AuthData[0]}", "accept": "application/json", "content-type": "application/json", "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ""(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")}) as g:
        r = await g.post(URL, timeout=30, data='"{}"'.encode("utf-8"))
        print("Claim Status:", r.status_code)
        print("Claim Body", r.text)

def iterate():
    run(authenticate())
    run(claim_coins())
    
if __name__ == "__main__":
    while True:
        iterate()
        sleep(1805)