#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def get_crawl_data():
    data_arr = []
    # 급상승 검색어 상세 옵션은 모두 0으로 세팅한 조건 URL 입니다.
    url = "https://datalab.naver.com/keyword/realtimeList.naver?age=all&entertainment=-2&groupingLevel=0&marketing=-2&news=-2&sports=-2"
    headers = {'User-Agent' : 'tellmeit'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    for ah_item in soup.findAll('li', {'class':'ranking_item'}):
        rank = ah_item.find('span', {'class':'item_num'}).text
        title = ah_item.find('span', {'class':'item_title'}).text
        data_arr.append(title)
        if rank == "20":
            break
    return ",".join(data_arr)

def search_word(data, word):
    return data.find(word)
