# -*- coding: utf-8 -*-
import json
import random
import codecs
import argparse
import logging
import tweepy


def get_replies(replies_file_name):
    with codecs.open(replies_file_name, encoding='utf-8', errors='skip') as replies_file:
        return [reply for reply in replies_file]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File with list of replies', required=True)
    parser.add_argument('-a', '--auth_credentials', help='Authentication credentials', required=True)
    parser.add_argument('-u', '--user', help='User that will receive replies', required=False)
    return vars(parser.parse_args())


def get_api(auth_credentials_file_name):
    with open(auth_credentials_file_name) as auth_credentials_file:
        cred = json.loads(auth_credentials_file.read())
        auth = tweepy.OAuthHandler(cred['consumer_key'], cred['consumer_secret'])
        auth.secure = True
        auth.set_access_token(cred['access_token'], cred['access_token_secret'])
        api = tweepy.API(auth)
    return api


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, user, replies):
        super(MyStreamListener, self).__init__()
        self.user = user
        self.replies = replies

    def on_status(self, status):
        if not hasattr(status, 'retweeted_status') and not status.in_reply_to_status_id:
            logging.info('replying to tweet #{0}'.format(status.id))
            api.update_status('@{0}\n{1}'.format(self.user.screen_name, random.choice(self.replies)), status.id)


if __name__ == '__main__':
    logging.basicConfig(filename='info.log', level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%a %b %d %H:%M:%S %Y')
    logging.info('start script')

    auth_cred = get_args()['auth_credentials']
    target_user_name = get_args()['user']
    replies = get_replies(get_args()['file'])

    api = get_api(auth_cred)

    target_user = api.get_user(target_user_name or 'dan_1k')
    myStreamListener = MyStreamListener(target_user, replies)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter([str(target_user.id)])
