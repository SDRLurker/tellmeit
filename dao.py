import pickle

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import sys
import os
from logger import get_logger

logger = get_logger(__name__)

class dao_pickle:
    def save_alarm(self, last_up, alarm_dict, ping_dict):
        with open('alarm.pic','wb') as f:
            pickle.dump([last_up, alarm_dict, ping_dict], f)
            logger.info("save %d %s %s" % (last_up, alarm_dict, ping_dict) )

    def load_alarm(self):
        last_up = 0
        alarm_dict = {} 
        ping_dict = {} 
        if os.path.exists("alarm.pic"):
            f = open("alarm.pic", "rb")
            last_up, alarm_dict, ping_dict = pickle.load(f)
            logger.info("load %d %s %s" % (last_up, alarm_dict, ping_dict) )
            f.close()
        return last_up, alarm_dict, ping_dict

class dao_firebase:
    def __init__(self, firebase_key, url, bot_id):
        with open('t.json', 'w') as f:
            f.write(firebase_key)
        cred = credentials.Certificate('t.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL' : url
        })
        os.remove('t.json') 
        self.bot_id = bot_id
        
    def save_alarm(self, last_up, alarm_dict, ping_dict):
        ref = db.reference(self.bot_id)
        ref.update({'last_up':last_up, 'alarm':alarm_dict, 'ping':ping_dict})
        logger.info("save %d %s %s" % (last_up, alarm_dict, ping_dict) )

    def load_alarm(self):
        last_up = 0
        alarm_dict = {} 
        ping_dict = {} 
        ref = db.reference(self.bot_id)
        if ref.get():
            last_up = ref.get().get('last_up',0)
            alarm_dict = ref.get().get('alarm',{})
            ping_dict = ref.get().get('ping',{})
            logger.info("load %d %s %s" % (last_up, alarm_dict, ping_dict) )
        return last_up, alarm_dict, ping_dict

def __check_variable(v, name):
    if not v:
        logger.error('%s is not found.' % name)
        sys.exit(1)


if __name__ == "__main__":
    firebase_key = os.environ.get('FIREBASE_KEY','')
    #print(firebase_key)
    firebase_url = os.environ.get('FIREBASE_URL','')
    #print(firebase_key)
    bot_id = os.environ.get('TELEGRAM_BOT','')
    #print(bot_id)

    __check_variable(firebase_key, 'firebase_key')
    __check_variable(firebase_url, 'firebase_url')
    __check_variable(bot_id, 'bot_id')

    p = dao_pickle()
    last_up, alarm_dict, ping_dict = p.load_alarm()

    f = dao_firebase(firebase_key, firebase_url, bot_id)
    f.save_alarm(last_up, alarm_dict, ping_dict)
