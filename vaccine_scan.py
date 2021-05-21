import urllib3
import argparse
import json
from playsound import playsound
import datetime
import random
import time

'''
1. To get details about state codes of India:
https://cdn-api.co-vin.in/api/v2/admin/location/states
2. To get district codes in a state:
https://cdn-api.co-vin.in/api/v2/admin/location/districts/16
3. To get vaccine details by district and date
https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=265&date=10-05-2021
'''


def count_18plus_vaccine_scan(district):
    days = 0
    dt = datetime.datetime.now()
    while(days <= 2):
        dt_time = dt.strftime("%d-%m-%Y %H:%M:%S %Z%z")
        uri = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + str(district) + "&date=" + dt.strftime("%d-%m-%Y")
        print(uri)
        http = urllib3.PoolManager()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
            'X-Forwarded-For': '.'.join([str(random.randint(0,255)) for i in range(4)])
        }
        r = http.request('GET', uri, headers=headers)
        try:
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
        except:
            print("No data of slots on {} for district {}".format(dt.strftime("%d-%m-%Y"), district))
            print("--------------------------------")
        dt += datetime.timedelta(days=1)
        days += 1



def count_18plus_vaccine_scan_pincode(pincode):
    days = 0
    dt = datetime.datetime.now()
    while(days <= 2):
        dt_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S %Z%z")
        uri = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + str(pincode) + "&date=" + dt.strftime("%d-%m-%Y")
        print(uri)
        http = urllib3.PoolManager()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
            'X-Forwarded-For': '.'.join([str(random.randint(0,255)) for i in range(4)])
        }
        r = http.request('GET', uri, headers=headers)
        try:
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
                    print("For 18+: Pincode:{} and available center:{}".format(pincode,center))
                    print("################################")

                print("Time:{} pincode:{} Available capacity for 18+:{} Total availability:{}".format(dt_time,pincode,availability,total_availability))
                print("--------------------------------")
                playsound('./file_example_WAV_1MG.wav')
            else:
                print("Time:{} Pincode:{} Available capacity for 18+:{} Total availability:{}".format(dt_time,pincode,availability,total_availability))
                print("--------------------------------")
        except:
            print("No data of slots on {} for pincode {}".format(dt.strftime("%d-%m-%Y"), pincode))
            print("--------------------------------")
        dt += datetime.timedelta(days=1)
        days += 1


parser = argparse.ArgumentParser(description='''--Vaccine Slots Scanner--''')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--district', type=int, nargs='*', action='append', help='Add district codes')
group.add_argument('-p', '--pincode', type=int, nargs='*', action='append', help='Add pincode')
args = parser.parse_args()

if not args.pincode:
    while(True):
        #BBMP = 294
        #BLR_URBAN = 265
        #BLR_RULAR = 276
        try:
            for district in args.district[0]:
                count_18plus_vaccine_scan(district)
            time.sleep(30)
        except Exception as e:
            print(e)
            time.sleep(30)

else:
    while(True):
        try:
            for pincode in args.pincode[0]:
                count_18plus_vaccine_scan_pincode(pincode)
            time.sleep(30)
        except Exception as e:
            print(e)
            time.sleep(30)
