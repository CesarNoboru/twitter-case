import requests
import json
import urllib.parse
from log import logger
import time

def search(query):
    total = 0
    tweets = []
    users = []
    URL = "https://api.twitter.com/2/tweets/search/recent?query={}&tweet.fields=created_at,lang&max_results=100&expansions=author_id&user.fields=public_metrics,location"
    headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANUAKwEAAAAAqSfAa1p%2BYb%2Byfgc3Yo%2FC4efg8Yw%3DH8TFRh9WwZzkwsxwcyTJ8xd4qywTfn6JNFKKeCIMdGeISZWJWn'
    }
    dp_user = 0
    dp_tweet = 0
    for tag in query:
        logger.info(f"msg='Searching for tag' tag='{tag}'")
        start_time = time.time()
        surl = URL.format(urllib.parse.quote(tag))
        response = requests.request("GET", surl, headers=headers)
        payload = response.json()
        count_twt = 0
        count_usr = 0
        if 'data'in payload:
                
            for twt in payload['data']:
                row = [
                    twt['id'],
                    twt['author_id'],
                    twt['text'],
                    twt['created_at'],
                    twt['lang']
                ]
                if tweets.count(row) == 0:
                    tweets.append(row)
                    count_twt +=1
                else:
                    dp_tweet +=1
                
            for usr in payload['includes']['users']:
                if 'location' in usr:
                    location = usr['location']
                else:
                    location = 'Unknown'
                row = [
                    usr['id'],
                    usr['name'],
                    usr['username'],
                    usr['public_metrics']['followers_count'],
                    location
                ]
                if users.count(row) == 0:
                    users.append(row)
                    count_usr+=1
                else:
                    dp_user +=1

            seconds = time.time() - start_time
            logger.info(f"tweets={count_twt} users={count_usr} tag='{tag}' exc_time={seconds:.2f}")
        else:
            logger.warning(f"msg='No tweets for tag' tag='{tag}'")
        total = total + seconds
    usr_total = len(users)
    twt_total = len(tweets)
    query_total = len(query)
    logger.info(f"msg='Done searching' total_users={usr_total} duplicated_users={dp_user} total_tweets={twt_total} duplicated_tweets={dp_tweet} total_tags={query_total} total_exc_time={total:.2f} ")
    data = [users, tweets]
    return data