#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import pandas as pd
import numpy as np
import emoji
import contractions
import string
import joblib
import nltk
from nltk.tokenize import word_tokenize
#nltk.download('punkt')
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


def replace_retweet(tweet, default_replace=''):
    tweet = re.sub('RT\s+', default_replace, tweet)
    return tweet


def replace_user(tweet, default_replace='twitteruser'):
    tweet = re.sub('\B@\w+', default_replace, tweet)
    return tweet


def demojize(tweet):
    tweet = emoji.demojize(tweet)
    return tweet


def replace_url(tweet, default_replace=''):
    tweet = re.sub('(http|https):\/\/\S+', default_replace, tweet)
    return tweet


def replace_hashtag(tweet, default_replace=''):
    tweet = re.sub('#+', default_replace, tweet)
    return tweet


def to_lowercase(tweet):
    tweet = tweet.lower()
    return tweet


def word_repetition(tweet):
    tweet = re.sub(r'(.)\1+', r'\1\1', tweet)
    return tweet


def punct_repetition(tweet, default_replace=''):
    tweet = re.sub(r'[\?\.\!]+(?=[\?\.\!])', default_replace, tweet)
    return tweet


def fix_contractions(tweet):
    tweet = contractions.fix(tweet)
    return tweet


def custom_tokenize(
    tweet,
    keep_punct=False,
    keep_alnum=False,
    keep_stop=False,
    verbose=False,
    ):

    token_list = word_tokenize(tweet)
    if verbose:
        print('Post general tokenization: {}\n'.format(token_list))

    if not keep_punct:
        token_list = [token for token in token_list if token
                      not in string.punctuation]

    if verbose:
        print('Post punctuation removal: {}\n'.format(token_list))

    if not keep_alnum:
        token_list = [token for token in token_list if token.isalpha()]

    if not keep_stop:
        stop_words = set(stopwords.words('english'))
        stop_words.discard('not')
        stop_words.update(["'s"])
        token_list = [token for token in token_list if not token
                      in stop_words]

    if verbose:
        print('Post stopword removal: {}\n'.format(token_list))

    return token_list


def stem_tokens(tokens, stemmer):
    token_list = []
    for token in tokens:
        token_list.append(stemmer.stem(token))
    return token_list


def process_tweet(tweet, verbose=False):
    if verbose:
        print('Initial tweet: {}\n'.format(tweet))

    # # Twitter Features

    tweet = replace_retweet(tweet)  # replace retweet
    tweet = replace_user(tweet, '')  # replace user tag
    tweet = replace_url(tweet)  # replace url
    tweet = replace_hashtag(tweet)  # replace hashtag
    if verbose:
        print('Post Twitter processing tweet: {}\n'.format(tweet))

    # # Word Features

    tweet = to_lowercase(tweet)  # lower case
    tweet = fix_contractions(tweet)  # replace contractions
    tweet = punct_repetition(tweet)  # replace punctuation repetition
    tweet = tweet.replace('.', ' ')
    tweet = word_repetition(tweet)  # replace word repetition
    tweet = demojize(tweet)  # replace emojis
    if verbose:
        print('Post Word processing tweet: {}\n'.format(tweet))

    # # Tokenization & Stemming

    tokens = custom_tokenize(tweet, keep_alnum=True, keep_stop=False)  # tokenize
    stemmer = SnowballStemmer('english')  # define stemmer
    stem = stem_tokens(tokens, stemmer)  # stem tokens

    # lem = lemmatize_tokens(tokens, lemmatizer)

    return stem

def fit_tfidf(tweet_corpus):
    tf_vect = TfidfVectorizer(preprocessor=lambda x: x,
                              tokenizer=lambda x: x)
    tf_vect.fit(tweet_corpus)
    return tf_vect

def get_vectorizer(file):

    df = pd.read_csv(file)
    df['tokens'] = df['tweet_text'].apply(process_tweet)
    df['tweet_sentiment'] = df['sentiment'].apply(lambda i: (1 if i
            == 'positive' else 0))
    X = df['tokens'].tolist()
    y = df['tweet_sentiment'].tolist()
    (X_train, X_test, y_train, y_test) = train_test_split(X, y,
            random_state=0, train_size=0.80)
    tf = fit_tfidf(X_train)
    return tf

def load_model(file):

    model = joblib.load(file)
    return model
