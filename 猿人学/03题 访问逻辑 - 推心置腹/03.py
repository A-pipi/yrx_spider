import requests
import json


url = "https://match.yuanrenxue.cn/"
session = requests.session()
session.headers = {
    "sec-ch-ua-platform": "\"Windows\"",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": 'yuanrenxue',
    "accept": "application/json, text/javascript, */*; q=0.01",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Chromium\";v=\"148\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://match.yuanrenxue.cn/match/3",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "sessionid=fe6df1ykstch0l1gwsvqibef0eafbpdv",
    "priority": "u=0, i"
}


def send1():
    url1 = url + "api2/3"
    res = session.get(url1)
    # print(res)

def send2(page):
    url2 = url + "api/question/3"

    params = {
        'page': page,
        'pageSize': 10,
        "kw": ""
    }

    res = session.get(url2, params=params)
    # print(res)

    data = json.loads(res.text).get("data")

    print(i, data)

    sum = 0
    for item in data:
        sum += item

    return sum

if __name__ == '__main__':
    sum = 0
    for i in range(1, 6):
        send1()
        sum += send2(i)
    print(sum)
