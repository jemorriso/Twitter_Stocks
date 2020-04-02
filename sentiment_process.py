import pandas as pd
import numpy as np
import re
import sys
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag


def remove_pattern(input_txt, pattern):
    #print(input_txt)
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt


def filter_stop_words(word):
    stop_words = set(stopwords.words('english'))
    if word in stop_words:
        return False
    else:
        return True


def gen_wordcloud(df):
    # generate wordcloud
    all_words = ' '.join([text for text in tweets_df['tidy_text']])
    wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.savefig('worldcloud.png')


def gen_dataframe(f, utf8=True):
    if utf8:
        df = pd.read_csv(f)

    # the training data is not utf8 encoded and has no column headers
    else:
        df = pd.read_csv(f, encoding='ISO-8859-1', names=['target', 'ids', 'date', 'flag', 'user', 'text'])
    return df


# clean and lemmatize all the tweets in the dataframe and add new column with the word stems
def clean_tweets(df):
    lemmatizer = WordNetLemmatizer()

    # remove all username handles and append new column 'tidy_text'
    df['tidy_text'] = np.vectorize(remove_pattern)(df['text'], "@[\w]*")

    # remove special characters, numbers, punctuations
    df['tidy_text'] = df['tidy_text'].str.replace("[^a-zA-Z#]", " ")

    # tokenize tweets into lists of words
    tokenized_text = df['tidy_text'].apply(lambda x: x.split())
    # tokenized_text = word_tokenize(df['tidy_text'])

    # iterate over each list
    for i, tweet in tokenized_text.iteritems():
        # lowercase everything
        processed_tweet = [x.lower() for x in tweet]

        # remove stop words
        processed_tweet = list(filter(filter_stop_words, processed_tweet))

        lemmatized_tweet = []
        # POS (part of speech) tag each word for lemmatization (change each word into its canonical form)
        for word, tag in pos_tag(processed_tweet):
            wordnet_tag_prefix = tag[0].lower()

            # adjectives, nouns, verbs
            wordnet_tag_prefix = wordnet_tag_prefix if wordnet_tag_prefix in ['a', 'r', 'n', 'v'] else None

            lemmatized_tweet.append(word if not wordnet_tag_prefix else lemmatizer.lemmatize(word, wordnet_tag_prefix))

        tokenized_text[i] = lemmatized_tweet

    # replace tidy_texts with processed version
    for i in range(len(tokenized_text)):
        tokenized_text[i] = ' '.join(tokenized_text[i])

    df['tidy_text'] = tokenized_text
    return df


if __name__ == "__main__":
    # uncomment these the first time you run the program
    # nltk.download('stopwords')
    # nltk.download('wordnet')
    # nltk.download('averaged_perceptron_tagger')

    # take in csv file
    if len(sys.argv) > 1:
        tweets_df = gen_dataframe(sys.argv[1])
        tweets_df = clean_tweets(tweets_df)

        gen_wordcloud(tweets_df)





