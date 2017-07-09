#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def get_crawl_data():
    data_arr = []
    url = "https://www.naver.com"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    for ah_item in soup.findAll('li', {'class':'ah_item'}):
        rank = ah_item.find('span', {'class':'ah_r'}).text
        title = ah_item.find('span', {'class':'ah_k'}).text
        data_arr.append(title)
        if rank == "20":
            break
    return ",".join(data_arr)

def search_word(data, word):
    return data.find(word)
