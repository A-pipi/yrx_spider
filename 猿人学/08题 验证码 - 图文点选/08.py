from img import main
import time
import requests
import base64
import json


def get_xy(targets, arr):
    Position = {
        "0": {"x": 50,"y": 50},
        "1": {"x": 150,"y": 50},
        "2": {"x": 250,"y": 50},
        "3": {"x": 50,"y": 150},
        "4": {"x": 150,"y": 150},
        "5": {"x": 250,"y": 150},
        "6": {"x": 50,"y": 250},
        "7": {"x": 150,"y": 250},
        "8": {"x": 250,"y": 250},
    }

    res = []

    for target in targets:
        t = 0
        for obj in arr:
            if target == obj.get(str(t)):
                res.append(Position.get(str(t)))
                break
            t += 1
        if t == 9: return None

    return res


class Session:
    def __init__(self):
        self.id = None
        self.session = requests.session()
        self.session.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "cookie": "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1779001012; Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1780731259,1783231638; sessionid=2op20261dehuwjd7asnghz331b4nwexr",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://match.yuanrenxue.cn/match/8",
            "sec-ch-ua": "Not/A)Brand;v=99, Chromium;v=148",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        self.sum = 0


    def get_image(self):
        url = "https://match.yuanrenxue.cn/api2/8"
        params = {
            "t": int(time.time() * 1000)
        }
        res = self.session.get(url, params=params)

        targets = res.json().get("targets")
        image = res.json().get("image")
        self.id = res.json().get("id")

        open("img.webp", "wb").write(base64.b64decode(image.split(',')[1], validate=True))

        return targets


    def check(self, click):
        url = "https://match.yuanrenxue.cn/api2/8"
        data = {
            "captcha_id": self.id,
            "clicks": json.dumps(click, separators=(',', ':')),
        }
        res = self.session.post(url, data=data)

        return res.status_code


    def func(self):
        count = 0
        while True:
            count += 1
            targets = session.get_image()
            arr = main()

            suc = get_xy(targets, arr)
            if suc: break
        print(f"经过{count}次成功 ", suc)
        session.check(suc)


    def get_data(self):
        for i in range(1, 6):
            session.func()

            url = "https://match.yuanrenxue.cn/api/question/8"
            params = {
                "page": i,
                "pageSize": "10"
            }
            if i == 5:
                self.session.headers["user-agent"] = 'yuanrenxue'

            res = self.session.get(url, params=params)

            # print(res.json())

            ttt = res.json().get("data")

            print(f"第{i}页已完成", ttt)

            for item in ttt:
                self.sum += item
            # break


if __name__ == '__main__':
    session = Session()
    session.get_data()
    print(session.sum)
