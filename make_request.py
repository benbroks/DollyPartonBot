import requests
import urllib.parse
import os

import oauth2 as oauth
from requests_oauthlib import OAuth1
# from config import API_KEY, API_SECRET_KEY, OAUTH_TOKEN, OAUTH_TOKEN_SECRET




os.environ.get('API_KEY')
os.environ.get('API_SECRET_KEY')
os.environ.get('OAUTH_TOKEN')
os.environ.get('OAUTH_TOKEN_SECRET')
consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_SECRET_KEY')

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'

tweet_url = 'https://api.twitter.com/1.1/statuses/update.json'

spotify_url = "https://open.spotify.com/track/4w3tQBXhn5345eUXDGBWZG?si=WdxiaUBjTdKREsQ7g3qiLA"

def authorize():
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    # Step 1: Get a request token. This is a temporary token that is used for 
    # having the user authorize an access token and to sign the request to obtain 
    # said access token.

    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response {}".format(resp['status']))

    request_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))


    print ("Request Token:")
    print ("    - oauth_token        = {}".format(request_token['oauth_token']))
    print ("    - oauth_token_secret = {}".format(request_token['oauth_token_secret'])) 

    # Step 2: Redirect to the provider. Since this is a CLI script we do not 
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print ("Go to the following link in your browser:")
    print ("{0}?oauth_token={1}".format(authorize_url, request_token['oauth_token']))


    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = input('Have you authorized me? (y/n) ')
    oauth_verifier = input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the 
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this 
    # access token somewhere safe, like a database, for future use.
    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

    print ("Access Token:")
    print ("    - oauth_token        = {}".format(access_token['oauth_token']))
    print ("    - oauth_token_secret = {}".format(access_token['oauth_token_secret']))

    print ("You may now access protected resources using the access tokens above.") 

def tweet(msg):
    API_KEY=os.environ.get('API_KEY')
    API_SECRET_KEY=os.environ.get('API_SECRET_KEY')
    OAUTH_TOKEN=os.environ.get('OAUTH_TOKEN')
    OAUTH_TOKEN_SECRET=os.environ.get('OAUTH_TOKEN_SECRET')
    auth = OAuth1(API_KEY, API_SECRET_KEY, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    r = requests.post(tweet_url,auth=auth,data={"status":msg})

if __name__ == "__main__":
    msg = "working hard or hardly working? {}".format(spotify_url)
    tweet(msg)