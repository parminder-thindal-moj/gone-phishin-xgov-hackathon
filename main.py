### Import Libraries
from constants import GOV_API_KEY

import flask
from flask import Flask, request
from flask_app.extraction import url_extractor

import json
import pandas as pd
import pickle
import xgboost
import regex as re

import urllib.parse as urlparse
from tld import get_tld
import urllib.request as urlreq
import time

from notifications_python_client.notifications import NotificationsAPIClient
from utils import SPAM_MSG_ID, NOT_SPAM_MSG_ID, SPAM_THRESHOLD
from functions.preprocessing import get_all_received_texts, get_sms_id, get_user_phone_number, get_spam_score, get_spam_classification, set_sms_id_to_send, send_sms_msg, get_sms_msg


### Set the Notify API Client
notifications_client = NotificationsAPIClient(GOV_API_KEY)

### Get all the recieved texts
current_recieved_txts = get_all_received_texts(notifications_client)

# Set up the existing_sms_msgs
existing_sms_msgs = []

for sms in current_recieved_txts['received_text_messages']:
    existing_sms_msgs.append(sms['id'])


## Running the service

while True:
    msg = "Running GOV.UK SPAM SERVICE"
    print(msg)
    
    # Get texts
    all_sms_msgs = get_all_received_texts(notifications_client)
    
    recieved_sms_msgs = all_sms_msgs['received_text_messages']

    for sms in recieved_sms_msgs:

        if get_sms_id(sms) in existing_sms_msgs:
            break

        print(sms)
        
        try:
            # Get user sms text
            user_sms = get_sms_msg(sms=sms)
            print("Getting: " + user_sms)
            
            user_phone_number = get_user_phone_number(sms=sms)
            print(user_phone_number)
            
            # Get spam score
            spam_score = get_spam_score(user_sms)
            print(spam_score)
            
            # get spam classfication
            spam_classication = get_spam_classification(spam_score=spam_score, SPAM_THRESHOLD=SPAM_THRESHOLD)
            
            # get spam_sms_id to send:
            sms_to_send = set_sms_id_to_send(spam_classification=spam_classication)
            
            # send the sms msg back to the user
            send_sms_msg(NotificationsAPIClient=notifications_client, 
                         phone_number=user_phone_number, 
                         sms_id_to_send=sms_to_send)
            
            #Add to existing text message list
            existing_sms_msgs.append(get_sms_id(sms=sms))
            
        except Exception as e:
            print("some sort of error occurred, let's hope it's not important")
            print(e)

    time.sleep(1)
  
# if __name__ == "__main__":
#     msg = "Running the GOV.UK SPAM SERVICE"
#     print(msg)
    