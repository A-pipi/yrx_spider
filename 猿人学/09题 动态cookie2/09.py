import time
import requests
import execjs
import json


sum = 0
for i in range(1, 6):
    # f = open("09.js", "r", encoding="utf-8")
    # js_code = f.read()
    # f.close()
    # js = execjs.compile(js_code)
    # m = js.call("encrypt", int(time.time() * 1000))
    # print(m)
    m = 2

    url = f"https://match.yuanrenxue.cn/api/question/2"

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": f"Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1779001012; Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1780731259,1783231638; sessionid=2op20261dehuwjd7asnghz331b4nwexr; m={m}",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://match.yuanrenxue.cn/match/9",
        "sec-ch-ua": "Not/A)Brand;v=99, Chromium;v=148",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    params = {
        "page": i,
        "pageSize": "10",
        "kw": ""
    }

    if i == 5:
        headers["user-agent"] = 'yuanrenxue'

    res = requests.get(url, headers=headers, params=params)
    print(res.json())
    # data = res.json().get("data")
    #
    # print(i, data)
    #
    # for item in data:
    #     sum += item
    break
print(sum)

