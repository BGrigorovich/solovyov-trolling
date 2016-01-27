# -*- coding: utf-8 -*-
import json
import random
import codecs
import logging
import tweepy
import click


def get_replies(replies_file_name):
    with codecs.open(replies_file_name, encoding='utf-8', errors='skip') as replies:
        return [reply for reply in replies]


def get_api(auth_credentials_file_name):
    with open(auth_credentials_file_name) as auth_credentials_file:
        cred = json.loads(auth_credentials_file.read())
        auth = tweepy.OAuthHandler(cred['consumer_key'], cred['consumer_secret'])
        auth.secure = True
        auth.set_access_token(cred['access_token'], cred['access_token_secret'])
        api = tweepy.API(auth)
    return api


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, user, replies):
        super(MyStreamListener, self).__init__()
        self.user = user
        self.replies = replies
        self.api = api

    def on_status(self, status):
        if not hasattr(status, 'retweeted_status') and not status.in_reply_to_status_id:
            logging.info('replying to tweet #{0}'.format(status.id))
            self.api.update_status('@{0}\n{1}'.format(self.user.screen_name, random.choice(self.replies)), status.id)


@click.command()
@click.option('-f', '--replies_file', help='File with list of replies')
@click.option('-a', '--auth_credentials', help='Authentication credentials')
@click.option('-u', '--user', help='User that will receive replies', default='dan_1k')
def main(replies_file, auth_credentials, user):
    logging.basicConfig(filename='info.log', level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%a %b %d %H:%M:%S %Y')
    logging.info('start script')

    api = get_api(auth_credentials)
    replies = get_replies(replies_file)
    target_user = api.get_user(user)

    stream_listener = MyStreamListener(api, target_user, replies)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter([str(target_user.id)])

if __name__ == '__main__':
    main()
