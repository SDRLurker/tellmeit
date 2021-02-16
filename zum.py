#-*- coding: utf-8 -*-
import requests

def get_crawl_data():
    data_arr = []
    url = "https://search.zum.com/issue.zum"
    headers = {'User-Agent' : 'tellmeit'}
    res = requests.get(url, headers=headers, timeout=10)
    issue = res.json().get("issue",[])
    for item in issue:
        data_arr.append(item.get("keyword",""))
    return ",".join(data_arr)

def search_word(data, word):
    return data.find(word)

def get_search_tmpl():
    ALARM_TMPL = '''%s 검색어 확인
https://search.zum.com/search.zum?query=%s&qm=g_real1.top&real1_id=11&real1_type=unfold&method=uni&option=accu'''
    return ALARM_TMPL
