import requests
import execjs
from font import extract_text_from_font


def get_num(obj, data):
    sum = 0

    for item in data:
        mmm = 0
        for i in range(0, len(item), 7):
            s = item[i : i + 7]
            for j in obj:
                if s == j:
                    if obj[j] == 'o': obj[j] = '0'
                    mmm = mmm * 10 + int(obj[j])
        sum += mmm

    print(sum)

    return sum


def get_pho(woff):
    f = open("07.js", "r", encoding="utf-8")
    js_code = f.read()
    f.close()
    js = execjs.compile(js_code)
    js.call("de", woff)


def get_base():
    sum = 0

    for i in range(1, 6):

        url = "https://match.yuanrenxue.cn/api/question/7"

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "cookie": "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1779001012; Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1780731259,1783231638; sessionid=2op20261dehuwjd7asnghz331b4nwexr",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://match.yuanrenxue.cn/match/7",
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
            "pageSize": "10",
            "kw": ""
        }

        res = requests.get(url, headers=headers, params=params)

        woff = res.json().get("woff")
        data = res.json().get("data")

        get_pho(woff)

        obj = extract_text_from_font("font.woff")


        sum += get_num(obj, data)

    print(sum)



if __name__ == '__main__':
    get_base()