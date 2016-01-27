#!/bin/bash

source /home/bogdan/.virtualenvs/twitter_env/bin/activate
cd /home/bogdan/PycharmProjects/solovyov-trolling/core/
python twitter.py -f replies.txt -a auth_credentials.json -u bgrigorovich
