import flask
from flask import Flask, request
import json
import pandas as pd
import pickle
import xgboost
from flask_app.extraction import url_extractor

import regex as re
import urllib.parse as urlparse
import urllib.request as urlreq

from flask_app.app import score


def get_spam_score(url):
    """Get the spam score of a given url"""
    
    # Convert to features df
    data = url_extractor(url)
    
    # Load model
    model = pickle.load(open('xg_model.pkl', 'rb'))
    
    spam_score = round(model.predict_proba(data.to_numpy())[0][1], 2)

    return spam_score

def get_spam_classification(spam_score:float, threshold:float=0.65):
    """Get the text classfication or a spam score"""
    if spam_score >= threshold:
        spam_classfication = "SPAM"
    else:
        spam_classfication = "NOT SPAM"
    
    return spam_classfication