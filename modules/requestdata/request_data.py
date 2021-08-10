import requests
import parsel
import time
from modules import useragent

def request_from(url, apparent_encoding=False):
    time.sleep(1)
    headers = {'User-Agent': useragent.getUserAgent()}
    resp = requests.get(url, headers=headers)
    if apparent_encoding:
        resp.encoding = resp.apparent_encoding  # 自动识别编码
    return parsel.Selector(resp.text)  # 返回一个parsel Selector的对象  resp.text是获取html网页数据
