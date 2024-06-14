import requests
import base64
import time
from fake_useragent import UserAgent


class CoinGecko:
    def __init__(self, email: str, password: str, proxy: str):
        self.auth_token = self.user_id = None
        self.email = email
        self.password = password

        self.proxyLogin = proxy.split("@")[0].split(":")[0]
        self.proxyPass = proxy.split("@")[0].split(":")[1]
        self.proxyAddress = proxy.split("@")[1].split(":")[0]
        self.proxyPort = proxy.split("@")[1].split(":")[1]

        self.proxy = {"http":f"http://{proxy}"} if proxy is not None else None

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ua-UA,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'api.qna3.ai',
            'Origin': 'https://qna3.ai',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers',
            'User-Agent': UserAgent(os='windows').random,
            'x-lang': 'english',
        }

        self.user_agent = headers["User-Agent"]
        self.session = requests.Session()


    async def login(self):
        url = "https://www.coingecko.com"
        resp = self.session.get(f"{url}/accounts/csrf_meta.json", proxies=self.proxy)
        token = resp.json()["token"]
        data = {
            "authenticity_token": token,
            "user[email]": self.email,
            "user[password]": self.password
        }

        resp = self.session.post(url=f"{url}/account/sign_in?locale=en", data=data, proxies=self.proxy)
        print(f"Login response status: {resp.status_code}")
        html_content = resp.text
        html_base64 = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")

        Api_key = "API KEY"

        task_payload = {
            "clientKey":Api_key,
            "task": {
                "type":"TurnstileTask",
                "websiteURL":url,
                "websiteKey":"xxxxxxxxxx",
                "cloudflareTaskType": "cf_clearance",
                "htmlPageBase64": html_base64,
                "userAgent": self.user_agent,
                "proxyType":"http",
                "proxyAddress":self.proxyAddress,
                "proxyPort":self.proxyPort,
                "proxyLogin":self.proxyLogin,
                "proxyPassword":self.proxyPass
            }
        }

        task_response = self.session.post("https://api.capmonster.cloud/createTask", json=task_payload)
        task_id = task_response.json().get("taskId")
        print("taskId = ", task_id)

        solution = None
        while not solution:
            time.sleep(5)
            solution_response = requests.post("https://api.capmonster.cloud/getTaskResult", json={"clientKey": Api_key, "taskId":task_id}, proxies=self.proxy)
            print(solution_response.json())
            if solution_response.json().get("status") == "ready":
                solution = solution_response.json().get("solution")

        print('Success')

        
    async def logout(self):
        await self.session.close()
