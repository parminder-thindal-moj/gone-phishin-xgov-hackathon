import flask
from flask import Flask, request
import json
import pandas as pd
import pickle
import xgboost
from flask_app.extraction import url_extractor
from flask_cors import CORS
import regex as re

import urllib.parse as urlparse
from tld import get_tld
import urllib.request as urlreq

app = Flask(__name__)
CORS(app)

@app.route("/score", methods=['POST'])
def score():
    
    # Get url
    url =  request.json['url']
    
    # Convert to features df
    data = url_extractor(url)
    
    # Load model
    model = pickle.load(open('xg_model.pkl', 'rb'))

    return str(model.predict_proba(data.to_numpy())[0][1])
