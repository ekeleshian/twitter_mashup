import flask
from flask import Flask
from flask import render_template
from main import main
import pickle
import random

app = Flask(__name__, template_folder='template')
user_names = ""

tweet_dict = dict()
count_dict = dict()

user_names = ["Alyssa_Milano", "annakhachiyan", "FINALLEVEL", "kanyewest", "realDonaldTrump"]

for idx in range(len(user_names)):
    for jdx in range(idx+1, len(user_names)):
        user_one = user_names[idx]
        user_two = user_names[jdx]
        with open(f"data/{user_one}__{user_two}__tweets__v4.pkl", "rb") as file:
            tweets = pickle.load(file)
        tweet_dict[f'{user_one}__{user_two}'] = tweets

@app.route('/')
def hello_world():
    names = ["Alyssa_Milano", "annakhachiyan", "FINALLEVEL", "kanyewest", "realDonaldTrump"]
    return render_template('index.html', names=names)


@app.route("/submit/<user_1>/<user_2>",  methods=["GET", "POST"])
def left(user_1, user_2):
    print(f"user_1 {user_1}")
    print(f"user_2 {user_2}")
    count = count_dict.get(f'{user_1}__{user_2}', None)

    if count:
        count_dict[f'{user_1}__{user_2}'] += 1
    else:
        count_dict[f'{user_1}__{user_2}'] = 1
        count = 1

    if count > 15:
        main(user_1, user_2)

    max_range = len(tweet_dict[f'{user_1}__{user_2}'])

    random_idx = random.randint(0, max_range-1)

    tweet = tweet_dict[f'{user_1}__{user_2}'][random_idx]
    print(tweet)
    return flask.json.jsonify(tweet)

