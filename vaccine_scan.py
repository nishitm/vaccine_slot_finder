import urllib3
import json
from playsound import playsound
from datetime import datetime
import time

'''
1. To get details about state codes of India:
https://cdn-api.co-vin.in/api/v2/admin/location/states
2. To get district codes in a state:
https://cdn-api.co-vin.in/api/v2/admin/location/districts/16
3. To get vaccine details by district and date
https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=265&date=10-05-2021
'''


def count_18plus_vaccine_scan(district):
    dt = datetime.now().strftime("%d-%m-%Y")
    dt_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S %Z%z")
    uri = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=" + str(district) + "&date=" + dt
    print(uri)
    http = urllib3.PoolManager()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
    r = http.request('GET', uri, headers=headers)
    slots = json.loads(r.data)
    centers = slots['centers']
    availability = 0
    total_availability = 0
    available_center_name=set()
    for center in centers:
        for session in center['sessions']:
            total_availability += session['available_capacity']
            if(session['min_age_limit'] == 18):
                availability += session['available_capacity']
                available_center_name.add(center['name'])
    if availability > 0:
        for center in available_center_name:
            print("################################")
            print("For 18+: District:{} and available center:{}".format(district,center))
            print("################################")

        print("Time:{} District:{} Available capacity for 18+:{} Total availability:{}".format(dt_time,district,availability,total_availability))
        print("--------------------------------")
        playsound('./file_example_WAV_1MG.wav')
    else:
        print("Time:{} District:{} Available capacity for 18+:{} Total availability:{}".format(dt_time,district,availability,total_availability))
        print("--------------------------------")


while(True):
    BBMP = 294
    BLR_URBAN = 265
    BLR_RULAR = 276
    try:
        count_18plus_vaccine_scan(BLR_URBAN)
        count_18plus_vaccine_scan(BBMP)
        count_18plus_vaccine_scan(BLR_RULAR)
        time.sleep(30)
    except Exception as e:
        print(e)
        time.sleep(30)
