import sys
import pandas as pd


def generate_csv(users):
    df = pd.read_csv("data/clean_tweets_rdt_kw_icet_am_ak.csv")
    tweets = list(df[df['user'] == users[0]]['cleaner_tweet'])
    tweets.extend(list(df[df['user'] == users[1]]['cleaner_tweet']))
    df_part = pd.DataFrame({'tweet': tweets})
    df_part = df_part.sample(frac=1)
    df_part.to_csv(f"data/{users[0]}_{users[1]}_tweets.csv", index=False, header=False)


if __name__ == '__main__':
    users = sys.argv[1:]
    generate_csv(users)