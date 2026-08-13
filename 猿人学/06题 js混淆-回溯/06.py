import time
import requests
import execjs

session = requests.Session()

sum = 0
s = ""

for i in range(1, 6):

    t = int(time.time()) * 1000

    f = open("06.js", "r", encoding="utf-8")
    js_code = f.read()
    f.close()
    js = execjs.compile(js_code)
    data = js.call("en", t, i)

    s += "1-" + str(t) + "|"

    url = "https://match.yuanrenxue.cn/api/question/6"

    headers = {
        "application/json,": "text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1779001012; Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1780731259,1783231638; sessionid=5uga8asoqp32mm4tv42cpo9kgfnfiio7",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://match.yuanrenxue.cn/match/6",
        "sec-ch-ua": "Not/A)Brand;v=99, Chromium;v=148",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    if i == 5:
        headers["user-agent"] = 'yuanrenxue'

    params = {
        "page": i,
        "m": data,
        "q": s
    }

    res = session.get(url, headers=headers, params=params)
    print(res.json())
    print(res.url)

    ttt = res.json().get("data")

    print(i, ttt)

    for item in ttt:
        sum += item
    # break

print(sum)
