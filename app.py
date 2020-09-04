#!/usr/bin/env python3
import os
#Import server stuff
from flask import Flask, redirect
from flask import request
from flask import jsonify
#Import stuff for scraping
from bs4 import BeautifulSoup
from urllib.request import urlopen
#Import other stuff
import hashlib
import time
import json
#CORS
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

use_sheets = True
c = 0

version = 3

ruokalista = ""
last_updated = 1598534304.6135302
update_threshold = 3600

shee = {}
splits_last_updated = 1598534304.6135302
splits_update_threshold = 3600

ksyk_url = "https://ksyk.fi"
splits_url = "https://koulusfi.herokuapp.com/api/splits"
repo_url = "https://github.com/jonnelafin/KsykRuoka-api"

def getMenu():
    page = urlopen(ksyk_url).read()
    soup = BeautifulSoup(page)
    matches = soup.find_all("div", class_="et_pb_tab_content")
    out = []
    for x in matches:
        children = x.findChildren("p" , recursive=False)
        for i in children:
            out.append( str(i.get_text(" \n ")) )
#    print(children)
    return out#str(children[0].get_text(" \n "))
def now():
    return time.time()
def updateData():
    global last_updated, ruokalista
    now = time.time()
    diff = -(last_updated - now)
#    print(diff)
    if diff > update_threshold:
        print("Updating menu...")
        ruokalista = getMenu()
        last_updated = now
        print("Menu updated.")
    return diff

#Holders
normalL = []
splitL = []
splitL_low = []

def getSplits():
    global splits_url
    try:
        splits_url = os.environ['splits_url']
    except Exception as e:
        print("\"splits_url\" not set as an environ, the default url \"" + str(splits_url) + "\" will be used.")
    page_json = urlopen(splits_url).read()
    s = json.loads(page_json)
    print("Splits loaded: " + str(s))
    print("monday sample: " + s["data"]["MA"]["12.05-12.30"][0])
    return s["data"]
def updateSheets():
    global use_sheets, shee, normalL, splitL, sheet_day_step, splitL_low
    normalL = []
    splitL = []
    splitL_low = []
    print("Updating split data...")
    u_s = False
    if use_sheets:
        try:
            shee = getSplits()
            for day in shee:
                print("Split lunches: ")
                splitToday = []
                normalToday = []
                for val in shee[day]["12.05-12.30"]:
                    if not "xL" in val:
                        continue
                    print(val)
                    splitToday.append(val.replace("/", " / "))
                print("Normal lunches: ")
                for val in shee[day]["12.30-12.55"]:
                    if not "xL" in val:
                        continue
                    print(val)
                    normalToday.append(val.replace("/", " / "))
                splitL.append(splitToday)
                normalL.append(normalToday)
                print("Lower Split lunches: ")
                splitToday_low = []
                for val in shee[day]["11.40-12.05"]:
                    if not "xL" in val:
                        continue
                    print(val)
                    splitToday_low.append(val.replace("/", " / "))
                splitL_low.append(splitToday_low)
            u_s = True
        except Exception as e:
            print("Splits could not be loaded, please confirm that the url is correct and you have the rights to use it. \nError: "+ str(e))
            u_s = False
#            raise(e)
    print("Split data updated.")
    return u_s
last_u_s = False
def check_sheets_update():
    global splits_last_updated, last_u_s
    now = time.time()
    diff = -(splits_last_updated - now)
    if diff > splits_update_threshold:
        last_u_s = updateSheets()
        splits_last_updated = now
    return last_u_s
def getUID(ip):
    return hashlib.sha256(str(ip).encode("utf8")).hexdigest()

@app.route('/')
def hello():
    global chat, version, use_sheets, shee
    uIp = request.access_route[0]
    uID = getUID(uIp)
    global c
    c = c + 1
    idle = updateData()
    u_s = check_sheets_update()
    return jsonify({'menu':ruokalista, 'recent_query_count':c, 'menu_time_since_last_update' : idle, 'menu_last_updated' : last_updated, 'menu_source_site':ksyk_url, 'menu_update_threshold':update_threshold, 'sheets_enabled':u_s, 'splits_last_updated': splits_last_updated, 'splits_update_threshold':splits_update_threshold, 'splits_time_since_last_update':(splits_last_updated - now())*-1, 'sheets_splitLunch':splitL, 'sheets_normalLunch':normalL, 'app_version':version, 'app_source':repo_url, 'sheets_lower_splitLunch':splitL_low}), 200
if __name__ == '__main__':
    updateData()
    updateSheets()
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
