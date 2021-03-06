#!/bin/python3
import logging
from http.client import HTTPConnection  # py3
import argparse
import datetime
import hashlib
import sys
import requests


parser = argparse.ArgumentParser()
parser.add_argument('--search_all',
                    help="Search all districts in India ?",
                    type=bool,
                    default=False)
parser.add_argument('--d',
                    help="How many days from today do you want to be vaccinated",
                    type=int,
                    default=7)
parser.add_argument('--pincode',
                    help="Search within this particular pincode",
                    type=str,
                    default="xxxx")
parser.add_argument('--mobile',
                    help="Your Mobile Number",
                    type=str,
                    default="xxxxxx")
parser.add_argument('--secret',
                    help="Secret from your browser session")
args = parser.parse_args()




def debug_mode():
    log = logging.getLogger('urllib3')
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)
    HTTPConnection.debuglevel = 1

hold = "**********************************************"
# search all pincodes
SEARCH_ALL = args.search_all
#pincode you want to fetch results for
pincode = args.pincode
#your phone number
mobile = args.mobile
host = "https://cdn-api.co-vin.in"

def generate_otp(mobile):
    url = "/api/v2/auth/generateMobileOTP"
    #get secret from your browser session
    secret = "xxxxx"
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
    bearer_token = "Bearer " +  token
    headers = {"authorization": bearer_token}

    resp = requests.get(host + url, headers = headers)
    #print(resp.json())
    return resp

def get_slots_by_district(district_id, days_from_now):
    tomorrow = datetime.date.today() + datetime.timedelta(days=days_from_now)
    query_date = tomorrow.strftime("%d-%m-%Y")
    url = "/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + str(district_id) + "&date=" + query_date

    resp = requests.get(host + url)
    return resp

def parse_centers_response(resp):
    centers = resp.json()["centers"]
    if len(centers) > 0:
        for center in resp.json()["centers"]:
           center_name = center['name']
           sessions = center['sessions']
           is_min_age_45 = all( 45 == session['min_age_limit'] for session in sessions)
           if is_min_age_45:
               print(center_name, "-----", 'No Slots Found')
           else:
               print(center_name, "YYYYY", 'SLOT FOUND!!!')
    else:
        print("No Centers Found in Your pincode")


#debug_mode()

# Search all districts
if SEARCH_ALL:
    district_list = list(range(1, 501))
    for district in district_list:
        resp = get_slots_by_district(district, args.d)
        parse_centers_response(resp)
    sys.exit(0)


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
parse_centers_response(resp)
