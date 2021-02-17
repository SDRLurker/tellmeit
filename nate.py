#-*- coding: utf-8 -*-
import requests

def get_crawl_data():
    data_arr = []
    url = "https://www.nate.com/js/data/jsonLiveKeywordDataV1.js"
    headers = {'User-Agent' : 'tellmeit'}
    res = requests.get(url, headers=headers, timeout=10)
    keywords = res.json()
    for item in keywords:
        data_arr.append(item[1])
    return ",".join(data_arr)

def search_word(data, word):
    return data.find(word)

def get_search_tmpl():
    ALARM_TMPL = '''%s 검색어 확인
https://news.nate.com/search?q=%s'''
    return ALARM_TMPL
