import requests
import json

url = "https://match.yuanrenxue.cn/"
session = requests.session()


def send1():
    header = {
        "sec-ch-ua-platform": "Windows",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "accept": "*/*",
        "sec-ch-ua": "Not/A)Brand;v=99, Chromium;v=148",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://match.yuanrenxue.cn/match/3",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
    }
    cookie = {
        "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3": "1779001012",
        "Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0": "1778941146,1779000679,1779005543,1779581926",
        "HMACCOUNT": "316FD8398D3BEA37",
        "sessionid": "ar8irhwtqg15mx2mus39lbvtwz20yb3e",
        "m": "79abb7c188e2518d67512708a43c3c54",
        "RM4hZBv0dDon443M": "Sfzmacj/nLAso3+nSdy2YLc+WxP7ClcQe/2Q5SMK2014zh3rI1yOY7YQSBG+ZAclvv5kMWHj6CndEItVJP6bYDAncJyEOdTMm10Xh8hNsBOiwNIoVD3jd7j2r0L8f3iwrYCwZYaLSi8MRDMyLcYf8au0pqYGRrdMN8rFmDa/C+hBeHKbf+gW5V0nimhMvJgISjXwanHq1XCgW4AyhuzKq9rT7ksfN6iDx5XO5Bg5fWE=",
        "Hm_lpvt_f80b2b389f44bbfb3bfe1704817d44e0": "1779613570"
    }
    url1 = url + "api2/3"
    session.headers = header
    res = session.get(url1, cookies=cookie)
    print(res.text)

def send2(page):
    header = {
        "sec-ch-ua-platform": "Windows",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "sec-ch-ua": "Not/A)Brand;v=99, Chromium;v=148",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://match.yuanrenxue.cn/match/3",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
    }
    cookie = {
        "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3": "1779001012",
        "Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0": "1778941146,1779000679,1779005543,1779581926",
        "HMACCOUNT": "316FD8398D3BEA37",
        "sessionid": "ar8irhwtqg15mx2mus39lbvtwz20yb3e",
        "m": "79abb7c188e2518d67512708a43c3c54"
    }
    url2 = url + f"api/question/3?page={page}&pageSize=10&kw="
    session.headers = header

    if page == 5:
        header['user-agent'] = 'yuanrenxue'

    res = session.get(url2, cookies=cookie)
    print(res.text)

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