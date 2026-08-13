import requests
import ddddocr
import execjs
import re

session = requests.Session()

def get_flag(key, value):

    f = open("04.js", "r", encoding="utf-8")
    js_code = f.read()
    f.close()
    js = execjs.compile(js_code)
    m = js.call("encrypt", key, value)

    return m

def get_num(url):
    base = url.split(",")[-1].split('" class=')[0]

    ocr = ddddocr.DdddOcr(beta=True, show_ad=False)                   # 实例化 ddddocr 对象
    text = ocr.classification(base)                                   # 图像识别

    return text

def order_sum(arr):
    sum = 0

    tmp = []

    for i, item in enumerate(arr):
        new_pos = i + int(item[1])
        tmp.append((new_pos, item))

    # 按新位置排序
    tmp.sort(key=lambda x: x[0])
    new = [item for _, item in tmp]

    for item in new:
        sum = sum * 10 + item[0]

    return sum

def main(page):
    sum = 0

    url = f"https://match.yuanrenxue.cn/api/question/4?page={page}&pageSize=10&kw="

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1779001012; sessionid=pfbaql9kj35r40sh0blqriu4ua713fs4; Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1779860838,1780122825,1780267813,1780731259; HMACCOUNT=316FD8398D3BEA37; Hm_lpvt_f80b2b389f44bbfb3bfe1704817d44e0=1780739241",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://match.yuanrenxue.cn/match/4",
        "sec-ch-ua": "Not/A)Brand;v=99, Chromium;v=148",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    if page == 5:
        headers["user-agent"] = 'yuanrenxue'
    res = session.get(url, headers=headers)
    txt = res.json().get("info")
    k = res.json().get("key")
    v = res.json().get("value")

    flag = get_flag(k, v)

    obj1 = re.compile(r'<td>(?P<Num>.*?)</td>')
    obj2 = re.compile(r'<img src="(?P<num>.*?)" style="left:(?P<style>.*?)px">')

    result1 = obj1.finditer(txt)
    for j in result1:
        arr = []
        result2 = obj2.finditer(j.group("Num"))
        for k in result2:
            u = k.group("num")
            s = float(k.group("style")) // 8.5
            if flag in u:
                continue
            n = get_num(u)
            arr.append([int(n), s])
        # print(arr)
        sum += order_sum(arr)
    print(page, sum)
    return sum

if __name__ == '__main__':
    result = 0
    for i in range(1, 6):
        result += main(i)
    print(result)


