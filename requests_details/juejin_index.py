from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests,json


def get_page_index():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    data = {
        'client_type': 2608,
        'cursor': "eyJ2IjoiNjg2MDI1NzExMDE3ODM2NTQ1NCIsImkiOjEwMH0=",
        'id_type': 2,
        'limit': 20,
        'sort_type': 200
    }
    url = "https://apinew.juejin.im/recommend_api/v1/article/recommend_all_feed"
    try:
        response = requests.request("post", url, json=data, headers=headers)
        # response = requests.get(url+ urlencode(data))   发送urlencode请求
        if response.status_code == 200:
            return response.text
        return None
    except:
        print("请求失败")


if __name__ == "__main__":
    first_content = json.loads(get_page_index())
    if first_content and "data" in first_content.keys():
        for item in first_content.get('data'):
            # print()
            with open("juejin_first.txt", "a", encoding="utf-8") as f:
                f.write(item.get('item_info').get('article_info').get('title')+"\n")