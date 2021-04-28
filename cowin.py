#!/bin/python3
import logging
from http.client import HTTPConnection  # py3

def debug_mode():
    log = logging.getLogger('urllib3')
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)
    HTTPConnection.debuglevel = 1

import datetime
import hashlib
import sys
import requests

hold = "**********************************************"
#pincode you want to fetch results for
pincode = "560034"
#your phone number
mobile = "77xxxx"
host = "https://cdn-api.co-vin.in"

def generate_otp(mobile):
    url = "/api/v2/auth/generateMobileOTP"
    #get secret from your browser session
    secret = "xxxxxxxxxxxxx"
    raw_data = { "secret" : secret, "mobile" : mobile}

    resp = requests.post( host + url, json = raw_data)
    return resp

def validate_otp(txn_id, otp):
    url = "/api/v2/auth/validateMobileOtp"
    otp_hash =  hashlib.sha256(otp.encode('utf-8')).hexdigest()
    raw_data = {"otp" : otp_hash, "txnId": txn_id}

    resp = requests.post( host + url, json = raw_data)
    return resp

def get_slots(token, pincode):
    tomorrow = datetime.date.today() + datetime.timedelta(days=2)
    query_date = tomorrow.strftime("%d-%m-%Y")
    url = "/api/v2/appointment/sessions/calendarByPin?pincode=" + pincode + "&date=" + query_date
    bearer_token = "bearer " +  token
    headers = {"authorization": bearer_token}

    resp = requests.get(host + url, headers = headers)
    print(resp.json())
    return resp

print("Generating OTP for: ", mobile)
print(hold)
resp = generate_otp(mobile)
if resp.status_code != 200:
    print("Sending OTP failed. Going to exit ", resp)
    sys.exit()

txn_id = resp.json()["txnId"]

otp = input("Enter the OTP: ")
print("Validating OTP: ", otp)
resp = validate_otp(txn_id, otp)
if resp.status_code != 200:
    print("OTP verification failed. Going to exit")
    sys.exit()

token = resp.json()["token"]

print("Fetching Slots...")
resp = get_slots(token, pincode)
if resp.status_code != 200:
    print("Failed to get slots. Going to exit")
    sys.exit()

for center in slots["centers"]:
    center_name = center['name']
    sessions = center['sessions']
    is_min_age_45 = all( 45 == session['min_age_limit'] for session in sessions)
    if is_min_age_45:
        print(center_name, "-----", 'No Slots Found')
    else:
        print(center_name, "YYYYY", 'SLOT FOUND!!!')

