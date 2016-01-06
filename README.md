# solovyov-trolling

Script for sending reply on each new non-retweet and non-reply tweet of specified user.

<h1>Usage</h1>

1) Create new titter app

2) Create auth_credentials.json with your credentials 

    {
      "consumer_key": "xxx",
      "consumer_secret": "xxx",
      "access_token": "xxx",
      "access_token_secret": "xxx"
    }
    
3) Run script from terminal

    python twitter.py -f <file_with_replies> [-i=60|-u=dAn_1k]
