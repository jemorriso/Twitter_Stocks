import sys
import json
#import dtale
import pandas as pd


def dataframe_to_csv(arr):
    tweets_df = pd.DataFrame.from_dict(arr)
    # drop irrelevant columns from dataframe
    tweets_df.drop(columns=['has_media', 'img_urls', 'is_replied', 'is_reply_to', 'links', 'parent_tweet_id',
                            'reply_to_users', 'text_html', 'video_url'],
                            inplace=True)
    # drop any rows that have empty tweets for some reason
    tweets_df = tweets_df[tweets_df["text"] != ""]

    # rearrange columns
    cols = tweets_df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('timestamp_epochs')))
    cols.insert(1, cols.pop(cols.index('timestamp')))
    cols.insert(2, cols.pop(cols.index('text')))

    # recreate dataframe with reordered columns
    tweets_df = tweets_df[cols]

    tweets_df.sort_values('timestamp_epochs', inplace = True)

    # dump to csv
    # csv has same name as json file
    tweets_df.to_csv(tweets_file.replace('json', 'csv'))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            tweets_file = sys.argv[1]
            with open(tweets_file) as tweets:
                tweets_arr = json.load(tweets)
        except:
            raise Exception("file not found")

        dataframe_to_csv(tweets_arr)




