import pickle

tweet_dict = dict()
user_names = ["Alyssa_Milano", "annakhachiyan", "FINALLEVEL", "kanyewest", "realDonaldTrump"]

for idx in range(len(user_names)):
    for jdx in range(idx+1, len(user_names)):
        user_one = user_names[idx]
        user_two = user_names[jdx]
        with open(f"data/backup/{user_one}__{user_two}__tweets__v4.pkl", "rb") as file:
            tweets = pickle.load(file)
        mega_tweet_string = tweets[0]
        new_tweets = mega_tweet_string.split("<|endoftext|>")
        new_tweets = [tweet[len('|<|startoftext|>') + 1:] for tweet in new_tweets]

        with open(f"data/{user_one}__{user_two}__tweets__v4.pkl", "wb") as file:
            pickle.dump(new_tweets, file)
