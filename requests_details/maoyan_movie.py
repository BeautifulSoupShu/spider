# coding:utf-8
# 爬取猫眼电影榜单

import time, json, requests
from pyquery import PyQuery
from multiprocessing import Pool
from requests.exceptions import RequestException


# 获取页面数据
def get_one_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    try:
        respone = requests.get(url,headers)
        if respone.status_code != 200:
            return None
    except RequestException:
        return None
    return respone.text


# 解析页面数据
def parse_one_page(text):
    doc = PyQuery(text)
    for info in doc("dl.board-wrapper dd").items():
        dct = {}
        dct["index"] = info.find(".board-index").text()
        dct["name"] = info.find("p.name a").text()
        dct["star"] = info.find("p.star").text()
        dct["releasetime"] = info.find("p.releasetime").text()
        dct["score"] = info.find(".score").text()
        yield dct


# 写入文件
def write_to_file(content):
    with open("maoyan_data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(content,ensure_ascii=False)+"\n")


if __name__ == '__main__':
    url = "http://maoyan.com/board/4?offset={offset}"
    # for i in range(10):
    text = get_one_page(url.format(offset=20))
    print(text)
    for item in parse_one_page(text):
        write_to_file(item)

# https://apinew.juejin.im/recommend_api/v1/article/recommend_all_feed
# https://apinew.juejin.im/recommend_api/v1/article/recommend_all_feed