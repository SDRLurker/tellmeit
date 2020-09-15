import pickle

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from tellmeit import logger, get_update, alarm_dict, ping_dict
import sys
import os

class dao_pickle:
    def save_alarm(self):
        with open('alarm.pic','wb') as f:
            pickle.dump([get_update.last_up, alarm_dict, ping_dict], f)
            logger.info("save %d %s %s" % (get_update.last_up, alarm_dict, ping_dict) )

    def load_alarm(self):
        get_update.last_up = 0
        global alarm_dict
        global ping_dict
        if os.path.exists("alarm.pic"):
            f = open("alarm.pic", "rb")
            get_update.last_up, alarm_dict, ping_dict = pickle.load(f)
            logger.info("load %d %s %s" % (get_update.last_up, alarm_dict, ping_dict) )
            f.close()
        return get_update.last_up, alarm_dict, ping_dict

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
        
    def save_alarm(self):
        global alarm_dict
        global ping_dict
        ref = db.reference(self.bot_id)
        print("save",{'last_up':get_update.last_up, 'alarm':alarm_dict, 'ping':ping_dict})
        ref.update({'last_up':get_update.last_up, 'alarm':alarm_dict, 'ping':ping_dict})
        logger.info("save %d %s %s" % (get_update.last_up, alarm_dict, ping_dict) )

    def load_alarm(self):
        get_update.last_up = 0
        global alarm_dict
        global ping_dict
        ref = db.reference(self.bot_id)
        print(ref.get())
        if ref.get():
            get_update.last_up = ref.get().get('last_up',0)
            alarm_dict = ref.get().get('alarm',{})
            ping_dict = ref.get().get('ping',{})
            logger.info("load %d %s %s" % (get_update.last_up, alarm_dict, ping_dict) )
        return get_update.last_up, alarm_dict, ping_dict

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
    get_update.last_up, alarm_dict, ping_dict = p.load_alarm()

    f = dao_firebase(firebase_key, firebase_url, bot_id)
    f.save_alarm()
