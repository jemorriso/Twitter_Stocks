import sentiment_process
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix


def build_model(f):
    tweets_df = sentiment_process.gen_dataframe(f, False)

    pos_100 = tweets_df[:1000]
    neg_100 = tweets_df[-1000:]

    tweets_subset = pos_100.append(neg_100)
    tweets_subset.reset_index(inplace=True)

    tweets_subset = sentiment_process.clean_tweets(tweets_subset)

    X_train, X_test, y_train, y_test = train_test_split(tweets_subset['tidy_text'], tweets_subset['target'],
                                                        test_size=0.2)

    tweets_vectorizer = CountVectorizer()
    train_counts = tweets_vectorizer.fit_transform(X_train)

    transformer = TfidfTransformer()
    train_tfidf = transformer.fit_transform(train_counts)

    test_counts = tweets_vectorizer.transform(X_test)
    test_tfidf = transformer.transform(test_counts)

    clf = MultinomialNB()
    clf.fit(train_tfidf, y_train)

    y_pred = clf.predict(test_tfidf)
    print(accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    return { "clf": clf, "count vectorizer": tweets_vectorizer, "tdidf transformer": transformer }


if __name__ == "__main__":
    # take in csv file
    if len(sys.argv) > 1:
        build_model(sys.argv[1])