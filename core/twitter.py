# -*- coding: utf-8 -*-
import json
import random
import codecs
import argparse
from datetime import datetime
from time import sleep
import tweepy


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


def troll(replies, interval=60, target_user_name='dAn_1k'):
    for tweet in get_target_tweets(target_user_name):
        api.update_status('@{0} {1}'.format(target_user_name, random.choice(replies)), tweet.id)
    sleep(interval * 60)


def get_replies(replies_file):
    with codecs.open(replies_file, encoding='utf-8', errors='skip') as f:
        return [reply for reply in f]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File with list of replies', required=True)
    parser.add_argument('-u', '--user', help='User that will receive replies', required=False)
    parser.add_argument('-i', '--interval', help='Check interval in minutes', required=False)
    return vars(parser.parse_args())

if __name__ == '__main__':
    api = get_api()
    replies_file = get_args()['file']
    target_user = get_args()['user']
    interval = get_args()['interval']
    replies = get_replies(replies_file)
    while True:
        if target_user and interval:
            troll(replies, interval=interval, target_user_name=target_user)
        elif target_user and not interval:
            troll(replies, target_user_name=target_user)
        elif interval and not target_user:
            troll(replies, interval=interval)
        else:
            troll(replies)
