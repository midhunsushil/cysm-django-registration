#!/usr/bin/python
# -*- coding: utf-8 -*-

# Imports for sentiment analysis

import re
import pandas as pd
import numpy as np
import emoji
import contractions
import string
import joblib
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from lambdafun_fix import lambdafun_fix


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


# def fit_tfidf(tweet_corpus):
#     tf_vect = TfidfVectorizer(preprocessor=lambdafun_fix,
#                               tokenizer=lambdafun_fix)
#
#     lambdafun_fix.__module__ = "lambdafun_fix"
#     #TfidfVectorizer.__module__ = 'apps'
#     tf_vect.fit(tweet_corpus)
#     return tf_vect


# def fit_lr(X_train, y_train):
#     model = LogisticRegression()
#     model.fit(X_train, y_train)
#     return model

filename_tfidf_vector = "tfidf_vector.pkl"
filename_model_lr_tf = "model_lr_tf.pkl"
tfidf_vector_pickled = joblib.load(filename_tfidf_vector)
model = joblib.load(filename_model_lr_tf)


def predict_tweet_using_pickled(tweet):
    processed_tweet = process_tweet(tweet)
    print(processed_tweet)
    transformed_tweet = tfidf_vector_pickled.transform([processed_tweet])
    prediction = model.predict(transformed_tweet)
    proba = model.predict_proba(transformed_tweet)
    print("Probability of   sentiment:", proba[:, 1])
    print("Probability of - sentiment:", proba[:, 0])

    print(prediction)
    if prediction == 1:
        return "Prediction is positive sentiment"
    else:
        return "Prediction is negative sentiment"


print(predict_tweet_using_pickled("You look beautiful today"))
