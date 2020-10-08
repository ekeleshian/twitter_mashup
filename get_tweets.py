import os
import re
from pdb import set_trace
import pickle
import requests

def process_tweet_text(text):
    text = re.sub(r'http\S+', '', text)   # Remove URLs
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)  # Remove @ mentions
    text = text.strip(" ")   # Remove whitespace resulting from above
    text = re.sub(r' +', ' ', text)   # Remove redundant spaces

    # Handle common HTML entities
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    return text


def auth():
    return os.environ.get("TWITTER_AUTH_BEARER_TOKEN")


def create_url(max_id=None):
    if not max_id:
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=realDonaldTrump&count=200&include_rts=false"
    else:
        url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=realDonaldTrump&count=200&include_rts=false&max_id={max_id}"

    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    min_id = float('inf')
    all_tweets = []

    for jsn in json_response:
        text = jsn['text']
        id = jsn['id']
        text = process_tweet_text(text)

        if text != '':
            all_tweets.append(text)
        min_id = min(min_id, id)

    seen_ids = set()
    seen_ids.add(min_id)

    while len(all_tweets) < 3000:
        url = create_url(min_id)
        json_response = connect_to_endpoint(url, headers)

        for jsn in json_response:
            text = jsn['text']
            id = jsn['id']
            text = process_tweet_text(text)
            if text != '':
                all_tweets.append(text)
            min_id = min(min_id, id)

        if min_id in seen_ids:
            break
        else:
            seen_ids.add(min_id)
        print(min_id)
        print(len(all_tweets))

    with open('dtrump_tweets.pkl', 'wb') as file:
        pickle.dump(all_tweets, file)

    with open('dtrump_lastid.pkl', 'wb') as file:
        pickle.dump(min_id, file)



if __name__ == "__main__":
    main()