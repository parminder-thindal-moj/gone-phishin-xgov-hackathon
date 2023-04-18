import flask
from flask import Flask, request
import json
import pickle
import xgboost
# from utils.extraction import url_extractor

import urllib.parse as urlparse
from tld import get_tld
import urllib.request as urlreq

import pandas as pd
import regex as re

import urllib.parse as urlparse
from tld import get_tld
import urllib.request as urlreq
from flask_cors import CORS

def url_extractor(url):

    cols = ['qty_dot_url','qty_hyphen_url','qty_underline_url','qty_slash_url','qty_questionmark_url',
            'qty_equal_url','qty_at_url','qty_and_url','qty_asterisk_url','qty_tld_url','length_url',
            'qty_dot_domain','qty_hyphen_domain','qty_vowels_domain','domain_length','qty_dot_directory',
            'qty_hyphen_directory','qty_underline_directory','qty_slash_directory','qty_equal_directory',
            'qty_at_directory','qty_and_directory','qty_asterisk_directory','qty_percent_directory',
            'directory_length','qty_dot_params','qty_hyphen_params','qty_underline_params','qty_slash_params',
            'qty_questionmark_params','qty_equal_params','qty_at_params','qty_and_params','qty_percent_params',
            'params_length','tld_present_params','qty_params','email_in_url'] 
    
    
    url_list = []

    if url[-1] == '/':
        url = url[:-1]

    myString = url
    url_test = re.search("(?P<url>https?://[^\s]+)", myString)

    if url_test is None:
        url_test = re.search("(?P<url>http?://[^\s]+)", myString)

    if url_test is None:
        url_test = re.search("(?P<url>www?[^\s]+)", myString)
    
    if url_test is None:
        return -1

    url_test = url_test.group("url")

    if url_test[0:3] == 'www':
        url_test = 'http://' + url_test

    url_list.append(url_test)

    new_df = []
    
    for url_test in url_list:

        underline_pattern = re.compile(r'__(.*?)__') 
        #url_test = str(url_test)
        path = urlparse.urlparse(url_test)

        whitelist = pd.read_csv("whitelist.csv")

        if path.netloc in whitelist['site'].to_list():
            return -1

        #Extracting column information

        qty_dot_url = url_test.count('.')
        qty_hyphen_url = url_test.count('-')
        qty_underline_url = re.findall(underline_pattern, url_test)
        qty_slash_url = url_test.count('/')
        qty_questionmark_url = url_test.count('?')
        qty_equal_url = url_test.count('=')
        qty_at_url = url_test.count('@')
        qty_and_url = url_test.count('&')
        qty_asterisk_url = url_test.count('*')
        qty_tld_url = url_test.count('~')
        length_url = len(url_test)

        if not qty_underline_url:
            qty_underline_url = 0

        qty_dot_domain = path.netloc.count('.')
        qty_hyphen_domain = path.netloc.count('-')
        qty_vowels_domain = len([char for char in path.netloc if char in "aeiouAEIOU"])
        domain_length = len(path.netloc)


        qty_dot_directory = path.path.count('.')
        qty_hyphen_directory = path.path.count('-')
        qty_underline_directory = re.findall(underline_pattern, path.path)
        qty_slash_directory = path.path.count('/')
        qty_equal_directory = path.path.count('=')
        qty_at_directory = path.path.count('@')
        qty_and_directory = path.path.count('&')
        qty_asterisk_directory = path.path.count('*')
        qty_percent_directory = path.path.count('%')
        directory_length = len(path.path)

        if not qty_underline_directory:
            qty_underline_directory = 0


        qty_dot_params = path.query.count('.')
        qty_hyphen_params = path.query.count('-')
        qty_underline_params = re.findall(underline_pattern, path.query)
        qty_slash_params = path.query.count('/')
        qty_questionmark_params = path.query.count('?')
        qty_equal_params = path.query.count('=')
        qty_at_params = path.query.count('@')
        qty_and_params = path.query.count('&')
        qty_percent_params = path.query.count('%')
        params_length = len(path.query)

        if not qty_underline_params:
            qty_underline_params = 0

        qty_params = 0
        if qty_dot_params > 0:
            qty_params = qty_params+1
        if qty_hyphen_params > 0:
            qty_params = qty_params+1
        if qty_underline_params > 0: 
            qty_params = qty_params+1
        if qty_slash_params > 0: 
            qty_params = qty_params+1  
        if qty_questionmark_params > 0:
            qty_params = qty_params+1 
        if qty_equal_params > 0:
            qty_params = qty_params+1 
        if qty_at_params > 0:
            qty_params = qty_params+1 
        if qty_and_params > 0:
            qty_params = qty_params+1 
        if qty_percent_params > 0:
            qty_params = qty_params+1 

        tld_present_params = get_tld(url_test)

        if len(tld_present_params) > 0:
            tld_present_params = 1
        else:
            tld_present_params = 0


        email_in_url = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', url_test)
        if len(email_in_url) > 0:
            email_in_url = 1
        else:
            email_in_url = 0


        #adding to df

        row1 = [qty_dot_url,qty_hyphen_url,qty_underline_url,qty_slash_url,qty_questionmark_url,qty_equal_url,
            qty_at_url,qty_and_url,qty_asterisk_url,qty_tld_url,length_url,qty_dot_domain,qty_hyphen_domain,
            qty_vowels_domain,domain_length,qty_dot_directory,qty_hyphen_directory,qty_underline_directory,
            qty_slash_directory,qty_equal_directory,qty_at_directory,qty_and_directory,qty_asterisk_directory,
            qty_percent_directory,directory_length,qty_dot_params,qty_hyphen_params,qty_underline_params,
            qty_slash_params,qty_questionmark_params,qty_equal_params,qty_at_params,qty_and_params,
            qty_percent_params,params_length,qty_params,tld_present_params,email_in_url] 

        new_df.append(row1)

    combined = pd.DataFrame(new_df, columns=cols)
    return combined

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    print("Received Hello world request")
    return "Hello, World!"

@app.route("/score", methods=['POST'])
def score():

    print(request.origin)

    # Get url
    url =  request.json['url']

    print("receievd url:" + str(url))
    
    # Convert to features df
    data = url_extractor(url)

    if type(data) is int:
        if data == -1:
            return "0"
        elif data == "-1":
            return "0"
    
    # Load model
    model = pickle.load(open('xg_model.pkl', 'rb'))

    return str(model.predict_proba(data.to_numpy())[0][1])

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)
