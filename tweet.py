from os import environ
from datetime import datetime, timedelta
import gspread
import tweepy
import time
from dotenv import load_dotenv
import app

load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

CONSUMER_KEY=environ['CONSUMER_KEY']
CONSUMER_SECRET=environ['CONSUMER_SECRET']
ACCESS_TOKEN=environ['ACCESS_TOKEN']
ACCESS_SECRET=environ['ACCESS_SECRET']







auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api= tweepy.API(auth)
gc=gspread.service_account(filename='new_credentials.json')
sh=gc.open_by_key('1Tg3GV9SVGOKutbKoSV9yGp_XwJ9pY_dN1rIcuHzfHFI')
worksheet=sh.sheet1

INTERVAL =int(environ['INTERVAL'])
DEBUG = environ['DEBUG']=='1'

def main():
    while True:
        tweet_records = worksheet.get_all_records()
        current_time = datetime.utcnow()  +  timedelta (hours=2)
        logger.info(f'{len(tweet_records)} tweets found at {current_time.time()}')
        
        for idx,tweet in enumerate(tweet_records, start=2):
            msg = tweet['message']
            time_str = tweet['time']
            done = tweet['done']
            date_time_obj = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
            if not done:
                now_time_cet = datetime.utcnow()  +  timedelta (hours=2)
                if date_time_obj < now_time_cet:
                    logger.info('this should be tweeted')
                    try:
                        api.update_status(msg)
                        worksheet.update_cell(idx,3, 1)
                    except Exception as e:
                        logger.warning(f'exception during tweet!{e}')
                        
                    
        
        
        time.sleep(INTERVAL)

if __name__=='__main__':
    main()