# -*- coding: utf-8 -*-
import json
import random
import codecs
import argparse
import logging
from datetime import datetime
from time import sleep
import tweepy


def str_now():
    return datetime.now().strftime('%a %b %d %H:%M:%S %Y')


def get_replies(replies_file):
    with codecs.open(replies_file, encoding='utf-8', errors='skip') as f:
        return [reply for reply in f]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File with list of replies', required=True)
    parser.add_argument('-u', '--user', help='User that will receive replies', required=False)
    parser.add_argument('-i', '--interval', help='Check interval in minutes', required=False)
    return vars(parser.parse_args())


def get_last_check_time():
    try:
        with open('last_check_time.txt') as f:
            return datetime.strptime(f.read(), '%a %b %d %H:%M:%S %Y')
    except (EnvironmentError, ValueError):
        return datetime.utcnow()


def set_last_check_time():
    with open('last_check_time.txt', 'w+') as f:
        f.write(datetime.utcnow().strftime('%a %b %d %H:%M:%S %Y'))


def get_api():
    with open('auth_credentials.json') as auth_credentials_file:
        cred = json.loads(auth_credentials_file.read())
        auth = tweepy.OAuthHandler(cred['consumer_key'], cred['consumer_secret'])
        auth.secure = True
        auth.set_access_token(cred['access_token'], cred['access_token_secret'])
        api = tweepy.API(auth)
    return api


def get_target_tweets(target_user_name):
    last_check_time = get_last_check_time()
    tweets = [tweet for tweet in api.user_timeline(target_user_name) if
              not hasattr(tweet, 'retweeted_status') and not tweet.in_reply_to_status_id and
              tweet.created_at > last_check_time]
    set_last_check_time()
    return tweets

def troll_default(default_interval, default_username):
    def troll(replies, interval, target_user_name):
        interval = interval or default_interval
        target_user_name = target_user_name or default_username
        for tweet in get_target_tweets(target_user_name):
            api.update_status('@{0}\n{1}'.format(target_user_name, random.choice(replies)), tweet.id)
            logging.info('{0} replying to tweet #{1}'.format(str_now(), tweet.id))
        sleep(float(interval) * 60)
    return troll


if __name__ == '__main__':
    logging.basicConfig(filename='info.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    api = get_api()
    replies_file = get_args()['file']
    target_user_name = get_args()['user']
    interval = get_args()['interval']
    replies = get_replies(replies_file)
    logging.info('{0} start script'.format(str_now()))
    solovyov_troll = troll_default(default_interval=60, default_username='dan_1k')
    while True:
        logging.info('{0} checking for new tweets'.format(str_now()))
        solovyov_troll(replies, interval, target_user_name)
