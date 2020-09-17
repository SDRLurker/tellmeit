#!/usr/bin/python3
#-*- coding: utf-8 -*-
import telegram # 텔레그램 모듈을 가져옵니다.

import os
import sys

import logging
import logging.handlers

import dao

alarm_dict = {}

pwd = os.getcwd()
if not os.path.exists('%s/log' % pwd):
    os.makedirs('%s/log' % pwd)
# logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
# fileHandler와 StreamHandler를 생성
fileHandler = logging.FileHandler('./log/notice.log')
# handler에 fommater 세팅
fileHandler.setFormatter(formatter)
# Handler를 logging에 추가
logger.addHandler(fileHandler)


def send_notice(bot, message):
    for chat_id in alarm_dict:
        bot.send_message( chat_id=chat_id, text=message )

def check_variable(v, name):
    if not v:
        logger.error('%s is not found.' % name)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("%s 메세지파일" % sys.argv[0])
        sys.exit(-1)

    f = open(sys.argv[1])
    s = f.read()
    f.close()

    firebase_key = os.environ.get('FIREBASE_KEY','')
    #print(firebase_key)
    firebase_url = os.environ.get('FIREBASE_URL','')
    #print(firebase_key)
    bot_id = os.environ.get('TELEGRAM_BOT','')
    #print(bot_id)
    my_token = os.environ.get('TELEGRAM_TOKEN','')
    #print(my_token)

    check_variable(firebase_key, 'firebase_key')
    check_variable(firebase_url, 'firebase_url')
    check_variable(bot_id, 'bot_id')
    check_variable(my_token, 'my_token')

    d = dao.dao_firebase(firebase_key, firebase_url, bot_id)

    bot = telegram.Bot(token = my_token)    # bot을 선언합니다.
    last_up, alarm_dict, ping_dict = d.load_alarm()
    send_notice(bot, s)
