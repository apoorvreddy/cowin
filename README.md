# cowin

This is a sample script to try out the cowin APIs. The APIs are public - https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2

You can configure the pincode and your mobile number, and the script will tell you if there's any center having vaccination slots for people below 45. I tried a few pincodes but could not find any. 

Usage:

```
python3 cowin.py --help
usage: cowin.py [-h] [--search_all SEARCH_ALL] [--d D] [--pincode PINCODE]
                [--mobile MOBILE]

optional arguments:
  -h, --help            show this help message and exit
  --search_all SEARCH_ALL
                        Search all districts in India ?
  --d D                 Within how many days do you want to be vaccinated
  --pincode PINCODE     Search within this particular pincode
  --mobile MOBILE       Your Mobile Number
```