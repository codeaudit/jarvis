#!/usr/bin/env python3
import jarvis
import os, dill

from crawler import tr_crawl, te_crawl
from cleaner import clean
from train_model import train
from test_model import test

training_tweets = jarvis.Action(func=tr_crawl) \
                        .produce(loc='training_tweets.csv', typ="data")

testing_tweets = jarvis.Action(func=te_crawl) \
                       .produce(loc='testing_tweets.csv', typ="data")

clean_training_tweets = jarvis.Action(func=clean, in_artifacts=[training_tweets]) \
                              .produce(loc='clean_training_tweets.pkl', typ='data')

clean_testing_tweets = jarvis.Action(func=clean, in_artifacts=[testing_tweets]) \
                             .produce(loc='clean_testing_tweets.pkl', typ='data')

intermediary = jarvis.Action(func=train, in_artifacts=[clean_training_tweets]) \
                     .produce(loc='intermediary.pkl', typ='model')

model_accuracy = jarvis.Action(func=test, in_artifacts=[intermediary, clean_testing_tweets])\
                       .produce(loc='model_accuracy.txt', typ='metadata')

model_accuracy.pull()

