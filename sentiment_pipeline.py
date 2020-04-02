import sys

from ts_to_csv import twitterscraper_to_csv
from sentiment_process import gen_dataframe, clean_tweets
from sentiment_model import build_model

query = sys.argv[1].split()

if "-o" in query:
    output_json = query[query.index("-o") + 1]
    output_csv = output_json.replace('json', 'csv')

#twitterscraper_to_csv(sys.argv)

tweets_df = gen_dataframe(output_csv)
cleaned_tweets_df = clean_tweets(tweets_df)

# training tweets are in sentiment140.csv
model_dict = build_model('sentiment140.csv')

# take our cleaned tweets data and count vectorize it
tweets_counts = model_dict['count vectorizer'].transform(cleaned_tweets_df['tidy_text'])
tweets_tfidf = model_dict['tdidf transformer'].transform(tweets_counts)

pred = model_dict['clf'].predict(tweets_tfidf)

# sentiment140.csv uses '4' for some reason
category_names = {'0': 'negative', '4': 'positive'}

pred_labels = [category_names[str(category)] for category in pred]
tweets_df['label'] = pred_labels

# print out results
for tweet, category in zip(cleaned_tweets_df['text'], pred):
    print('%r => %s' % (tweet, category_names[str(category)]))