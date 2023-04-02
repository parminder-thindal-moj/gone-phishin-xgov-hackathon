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
from functions.preprocessing import get_all_received_texts, get_sms_id, get_user_phone_number, get_all_sms_ids, get_spam_score, get_spam_classification, set_sms_id_to_send, send_sms_msg, get_sms_msg


### Set the Notify API Client
api_client = NotificationsAPIClient(GOV_API_KEY)

### Get all the recieved texts
all_sms_payload = get_all_received_texts(api_client)

# Get just the payload of all the recieved text msgs
recieved_sms_msgs = all_sms_payload['received_text_messages']

# Set up a list for the existing sms ids
existing_sms_ids = get_all_sms_ids(recieved_sms_msgs=recieved_sms_msgs)

## Running the service

while True:
    msg = "Running GOV.UK SPAM SERVICE"
    print(msg)
    
    # Get all the payload of all the recieved sms msgs
    all_sms_msgs_payload = get_all_received_texts(api_client)
    
    # Get just the payload of all the recieved text msgs
    recieved_sms_msgs = all_sms_msgs_payload['received_text_messages']
    
    for sms in recieved_sms_msgs:

        if get_sms_id(sms) in existing_sms_ids:
            break
        
        try:
            # Get user sms text
            user_sms = get_sms_msg(sms=sms)
            
            # Get the user phone number
            user_phone_number = get_user_phone_number(sms=sms)
            
            # Get spam score
            spam_score = get_spam_score(user_sms)

            # get spam classfication
            spam_classication = get_spam_classification(spam_score=spam_score, 
                                                        SPAM_THRESHOLD=SPAM_THRESHOLD)
            
            # get spam_sms_id to send:
            sms_to_send = set_sms_id_to_send(spam_classification=spam_classication)
            
            # send the sms msg back to the user
            send_sms_msg(NotificationsAPIClient=api_client, 
                         phone_number=user_phone_number, 
                         sms_id_to_send=sms_to_send)
            
            #Add to existing text message list
            existing_sms_ids.append(get_sms_id(sms=sms))
            
        except Exception as e:
            error_msg = "some sort of error occurred, let's hope it's not important"
            print(error_msg)
            print(e)

    time.sleep(1)
  
# if __name__ == "__main__":
#     msg = "Running the GOV.UK SPAM SERVICE"
#     print(msg)
    