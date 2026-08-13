import requests
import execjs
import json


sum = 0

for i in range(1, 6):
    f = open("01.js", "r", encoding="utf-8")
    js_code = f.read()
    f.close()
    js = execjs.compile(js_code)
    m = js.call("encrypt")
    print(m)

    url = f"https://match.yuanrenxue.cn/api/question/1"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1779001012; Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1780731259,1783231638; sessionid=fe6df1ykstch0l1gwsvqibef0eafbpdv; yuanrenxue_cookie=1786528970|2twysEib0230g22SJBkJzNmh66YvdwzrqCeE5A3tklthDcRDvoUrGzVP770ChCIRvJOD71GkJAZqUlV9qWZoSzcSW4SAdH9sOPwX2zmBv6Qxg0KSop42DxZ9K2sTlWpftOalmq0j7u3awYNznb9b2qc2Agyp7SPV1dbRht9bhhMl5ISQYVMxCYsYDL2sQSDrglQi1T7; m=1d45ed3890ae6ba42ca9b7046a662a49; RM4hZBv0dDon443M=PiLxeCjxbvaZ8qZldF80B6pbJXMmtJZcUwFAZcuHkiPZWhzWkwLf9dwrNP/Q27RZnzD5SpO3VNuOAbWYRD0mNsebPLYFGGzoUOMvPSUdL31u9F+YtlBsbW+YgCP5bK9zAqRD6Kuqq8oBeFRMhnCQS5Z+9WTn0kz5w8SxVJRnHQob0mPsh0/2jLsNRSKhkYVVq85+cIUxoiXOIUAxSXcu5nxVQVH8/emTcwCtesPNtQE=",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://match.yuanrenxue.cn/match/1",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Chromium\";v=\"148\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    params = {
        "page": i,
        "pageSize": "10",
        "kw": '',
        "m": m
    }

    if i == 5:
        headers["user-agent"] = 'yuanrenxue'

    res = requests.get(url, headers=headers, params=params)

    print(res.text)

    data = json.loads(res.text).get("data")

    print(i, data)

    for item in data:
        sum += item
    # break
print(sum)

