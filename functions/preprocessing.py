import flask
from flask import Flask, request
import json
import pandas as pd
import pickle
import xgboost
from flask_app.utils.extraction import url_extractor

import regex as re
import urllib.parse as urlparse
import urllib.request as urlreq

from utils import SPAM_MSG_ID, NOT_SPAM_MSG_ID, SPAM_THRESHOLD

def get_all_received_texts(NotificationsAPIClient):
    """Get all the recieved text messages to the digital phone number"""
    return NotificationsAPIClient.get_received_texts()


def get_sms_id(sms):
    """Get the sms id number"""
    sms_id_number = sms['id']
    return sms_id_number


def get_sms_msg(sms):
    """Get the user phone number from the sms msg"""
    sms = sms['content'].lower()
    return sms


def get_user_phone_number(sms):
    """Get the user phone number from the sms msg"""
    phone_number = sms['user_number']
    return phone_number


def get_all_sms_ids(recieved_sms_msgs:dict):
    """F to get all the sms ids"""
    sms_id_list = []
    for sms in recieved_sms_msgs:
        sms_id = get_sms_id(sms)
        sms_id_list.append(sms_id)
    return sms_id_list


def get_spam_score(url):
    """Get the spam score of a given url"""
    
    # Convert to features df
    data = url_extractor(url)

    """checking data type, to set score to 0 for urls in the whitelist"""
    if type(data) is int:
        if data == -1:
            return 0
        elif data == "-1":
            return 0
        
    # Load model
    model = pickle.load(open('xg_model.pkl', 'rb'))
    
    spam_score = round(model.predict_proba(data.to_numpy())[0][1], 2)

    return spam_score


def get_spam_classification(spam_score:float, SPAM_THRESHOLD:float=SPAM_THRESHOLD):
    """Get the text classfication of a spam score"""
    if spam_score >= SPAM_THRESHOLD:
        spam_classification = "SPAM"
    else:
        spam_classification = "NOT SPAM"
    
    return spam_classification


def set_sms_id_to_send(spam_classification):
    """Set which spam sms msg to send"""
    if spam_classification == "SPAM":
        sms_id_to_send = SPAM_MSG_ID
    elif spam_classification == "NOT SPAM":
        sms_id_to_send = NOT_SPAM_MSG_ID
    
    return sms_id_to_send


def send_sms_msg(NotificationsAPIClient, phone_number:int, sms_id_to_send:str):
    """Send sms msg to the user based on the outcome of the spam classification"""
    
    sms_msg = NotificationsAPIClient.send_sms_notification(
        phone_number = phone_number,
        template_id=sms_id_to_send
        )

    return sms_msg
