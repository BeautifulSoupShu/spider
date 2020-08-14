# coding:utf-8

import requests, os, re
from bs4 import BeautifulSoup
from bs4.element import Tag
from PIL import Image
from io import BytesIO
from multiprocessing import Pool

BASE_URL = "https://laogewen.vip"


def get_page_imgs(url, path,offsets):
    for offset in offsets:
        url_detail = url.format(offset=offset)
        _response = requests.get(url=url_detail)
        _soup = BeautifulSoup(_response.text, "lxml")
        _divs = _soup.find_all(name="div", attrs={"id": "posts"})
        for _index, div in enumerate(_divs):
            if isinstance(div,Tag) and _index is not 0:
                _imgs = div.find_all("img")
                for index, img in enumerate(_imgs):
                    img_url = BASE_URL + img.get('src')
                    img_response = requests.get(url=img_url)
                    img = Image.open(BytesIO(img_response.content)).convert('RGB')
                    img.save(path + "/lg_vip{}_{}.png".format(offset, index))


def get_zone_detail_lis(basedir, lis):
    for index, item in lis:
        if isinstance(item, Tag):
            city_detail = item.a.string
            city_detail_url = BASE_URL + item.a.get('href')[0:5]+"/page/"+ "{offset}"+ item.a.get('href')[5:]
            path_detail = basedir + "/" + city_detail
            pool = Pool(5)
            if not os.path.exists(path_detail):
                os.makedirs(path_detail)
                # get_page_imgs(city_detail_url, path_detail,[i for i in range(1, 51)])
                pool.apply_async(func=get_page_imgs,args=(city_detail_url,path_detail, [i*10 for i in range(1,50)]))
                pool.close()
                pool.join()
                pool.terminate()
                # pool.map(get_page_imgs, city_detail_url, [i*10 for i in range(1,50)])
            else:
                # pool = Pool()
                # pool.map(get_page_imgs, city_detail_url, [i * 10 for i in range(1, 50)])
                # get_page_imgs(city_detail_url, path_detail,[i for i in range(1,51)])
                pool.apply_async(func=get_page_imgs, args=(city_detail_url, path_detail, [i * 10 for i in range(1, 6)]))
                pool.close()
                pool.join()
                # pool.terminate()
                continue


def get_all_cities(soup):
    base_dir = "lg_vip/"
    zones = soup.find_all(name="div", class_=re.compile("^(city-inbox)"))
    for zone in zones:
        zone_div_detail = zone.find_all(name="div")[1]
        zone_name = zone.div.contents[0]
        path = base_dir + zone_name
        if os.path.exists(path):
            get_zone_detail_lis(path, enumerate(zone_div_detail.ul.children))
            continue
        else:
            os.makedirs(path)
            get_zone_detail_lis(path, enumerate(zone_div_detail.ul.children))


if __name__ == "__main__":
    response = requests.get("https://laogewen.vip/")
    soup = BeautifulSoup(response.text, "lxml")
    get_all_cities(soup)               #ul列表
