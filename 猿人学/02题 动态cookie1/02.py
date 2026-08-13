import time
import requests
import execjs
import json


sum = 0

for i in range(1, 6):
    f = open("02.js", "r", encoding="utf-8")
    js_code = f.read()
    f.close()
    js = execjs.compile(js_code)
    m = js.call("encrypt", int(time.time() * 1000))
    print(m)

    url = f"https://match.yuanrenxue.cn/api/question/2"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1779001012; Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1778941146,1779000679,1779005543,1779581926; HMACCOUNT=316FD8398D3BEA37; sessionid=ar8irhwtqg15mx2mus39lbvtwz20yb3e; Hm_lpvt_f80b2b389f44bbfb3bfe1704817d44e0=1779590409; m=" + m,
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://match.yuanrenxue.cn/match/2",
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
        'page': i,
        'pageSize': 10,
        'kw': ''
    }

    if i == 5:
        headers["user-agent"] = 'yuanrenxue'

    res = requests.get(url, headers=headers, params=params)
    # print(res.url)
    data = json.loads(res.text).get("data")

    print(i, data)

    for item in data:
        sum += item
    # break

print(sum)
