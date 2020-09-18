#!/usr/bin/python3
#-*- coding: utf-8 -*-
import telegram # 텔레그램 모듈을 가져옵니다.
import naver

import time
import datetime
import pickle
import os
from urllib.parse import quote
import sys
import psutil

import dao
from logger import get_logger

alarm_dict = {}
ping_dict = {}

HELP_MSG = """* /알람 (키워드1) (키워드2) ...
키워드1, 키워드2 (OR 조건) 등을 알람 메세지를 받을 수 있도록 등록합니다.
* /알람
등록된 키워드를 삭제합니다."""
ALARM_TMPL = '''%s 검색어 확인
https://search.naver.com/search.naver?where=nexearch&query=%s&ie=utf8&'''
PING_REG = "핑이 등록되었습니다."
PING_DEL = "핑이 해제되었습니다."
PING_MSG = "정각입니다. tellmeit_bot이 살아있음을 알립니다."

admin_id = os.environ.get('TELEGRAM_ADMIN','')
#print(admin_id)

logger = get_logger(__name__)

def is_valid_cmd(words, kcmd, cmd):
    is_cmd = len(words) >=1 and (words[0][1:] == kcmd or words[0][1:] == cmd)
    if is_cmd and words[0][0] == '/':
        return True
    return False

def parse_cmd(text):
    words = text.split()
    if len(words) >= 2 and (words[0] == "/알람" or words[0] == '/alarm'):
        return {'alarm':' '.join(words[1:])}
    elif is_valid_cmd(words, "알람", "alarm"):
        return {'alarm':''}
    if is_valid_cmd(words, "핑", "ping"):
        return {'ping':''}
    if is_valid_cmd(words, "도움", "help"):
        return {'help':HELP_MSG}
    return ""

def get_update(bot, dao):
    global alarm_dict
    global ping_dict
    try:
        updates = bot.getUpdates(get_update.last_up) # 업데이트 내역을 받아옵니다.
        logger.debug("get_update %d %d %s" % (get_update.last_up, len(updates), updates) )
        for u in updates :                           # 내역중 메세지를 출력합니다.
            msg = u.message
            if not u.message:
                msg = u.edited_message
            chat_id = str(msg.chat.id)
            text = msg.text

            cmd_dict = parse_cmd(text)
            if 'alarm' in cmd_dict:
                if cmd_dict['alarm'] == '':
                    alarm_dict.pop(chat_id, '')
                    bot.send_message(chat_id, '해당 키워드는 삭제되었습니다.')
                else:
                    alarm_dict[chat_id] = cmd_dict['alarm']
                    bot.send_message(chat_id, '%s 키워드가 등록되었습니다.' % cmd_dict['alarm'])
            elif 'help' in cmd_dict:
                bot.send_message(chat_id=chat_id, text=cmd_dict['help'])
            elif 'ping' in cmd_dict:
                if chat_id in ping_dict:
                    ping_dict.pop(chat_id, '')
                    bot.send_message(chat_id, PING_DEL)
                else:
                    ping_dict[chat_id] = chat_id
                    bot.send_message(chat_id, PING_REG)

            # https://github.com/python-telegram-bot/python-telegram-bot/issues/26
            get_update.last_up = u.update_id + 1
            dao.save_alarm(get_update.last_up, alarm_dict, ping_dict)
    except Exception as e:
        logger.error('get_update : ' + str(e))

# https://stackoverflow.com/questions/11329917/restart-python-script-from-within-itself
def restart_program():
    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logger.error('restart_program : ' + str(e))
    python = sys.executable
    os.execl(python, python, *sys.argv)

def send_ping(bot):
    for chat_id in ping_dict:
        bot.send_message( chat_id=chat_id, text=PING_MSG )

def send_alarm(bot):
    try:
        data = naver.get_crawl_data()
    except Exception as e:
        logger.error('send_alarm' + str(e))
        if admin_id:
            bot.send_message(admin_id, '네이버 크롤링 오류. 내용=%s' % str(e))
        return False
    for chat_id in alarm_dict:
        keywords = alarm_dict[chat_id].split()
        for keyword in keywords:
            logger.debug("send_alarm %s %s %s" % (chat_id, keyword, naver.search_word(data, keyword)) )
            if naver.search_word(data, keyword) >= 0:
                # send_message permission 오류로 except 처리 추가
                try:
                    bot.send_message( chat_id=chat_id, text= ALARM_TMPL % (keyword, quote(keyword)) )
                except Exception as e:
                    logger.error('bot.send_message(%s)' % chat_id + str(e))
    return True

def check_alarm(bot, dao):
    get_update(bot, dao)
    now = datetime.datetime.now()
    min = int(now.strftime("%M"))
    logger.debug("check_alarm %d %d %s" % (check_alarm.min, min, alarm_dict) )
    if check_alarm.min != min:
        logger.info("check_alarm.min %d, min %d" % (check_alarm.min, min) )
        logger.debug("alarm_dict %s" % (alarm_dict,) )
        if min == 0:
            send_ping(bot)
        check_alarm.min = min
        is_success = send_alarm(bot)
        if not is_success:
            restart_program()
    time.sleep(2)

def check_variable(v, name):
    if not v:
        logger.error('%s is not found.' % name)
        sys.exit(1)

if __name__ == "__main__":
    firebase_key = os.environ.get('FIREBASE_KEY','')
    #erint(firebase_key)
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
    get_update.last_up, alarm_dict, ping_dict = d.load_alarm()
    check_alarm.min = 0
    while True:
        check_alarm(bot, d)
