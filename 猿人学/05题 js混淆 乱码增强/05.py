import requests
import execjs

session = requests.Session()

sum = 0

f = open("05.js", "r", encoding="utf-8")
js_code = f.read()
f.close()
js = execjs.compile(js_code)
data = js.call("encrypt")

print(data.get("cook"))

for i in range(1, 6):

    url = f"https://match.yuanrenxue.cn/api/question/5?page={i}&m={data.get('t2')}&f={data.get('t1')}"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1779001012; Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1779860838,1780122825,1780267813,1780731259; sessionid=om0ktayxb59sx630zk9fggsj6ehuv5dx; " + data.get("cook"),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    }

    if i == 5:
        headers["user-agent"] = 'yuanrenxue'

    res = session.get(url, headers=headers)
    # print(res.json())

    ttt = res.json().get("data")

    print(i, ttt)

    for item in ttt:
        sum += item
    # break
print(sum)

