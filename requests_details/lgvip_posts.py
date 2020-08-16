# coding : utf-8

import requests, os, re
from bs4 import BeautifulSoup
from bs4.element import Tag
from PIL import Image
from io import BytesIO
from multiprocessing import Pool


BASE_URL = "https://laogewen.vip/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}


def get_page_imgs(url, page, index, pos):
    img_response = requests.get(url=url)
    img = Image.open(BytesIO(img_response.content)).convert('RGB')
    img.save("lgvip_posts/lg_vip{}_{}_{}.png".format(page, index, pos))


def get_images(url, page):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        div_content = soup.find_all(name="div", id="posts")
        for index, div_img in enumerate(div_content[1].find_all(name="div", class_="img")):
            url_detail = div_img.a.get('href')
            response_detail = requests.get(url=url_detail, headers=headers)
            soup_detail = BeautifulSoup(response_detail.text, 'lxml')
            blockquote = soup_detail.find(name="blockquote")
            for pos, img in enumerate(blockquote.find_all(name="img")):
                get_page_imgs(BASE_URL+img.get("src"), page, index, pos)
                # print(img.get('src'))


if __name__ == "__main__":
    for i in range(25, 501):
        url = "https://laogewen.vip/zjfb/page/" + str(i)
        pool = Pool(6)
        pool.apply_async(func=get_images, args=(url, i))
        pool.close()
        pool.join()
