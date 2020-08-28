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
#CORS
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

use_sheets = True
try:
    if use_sheets:
        from gsheets import Sheets
except Exception as e:
    print("FAILED importing gsheets, loading stuff automatically from the will be disabled.")
    use_sheets = False

c = 0

version = 1

ruokalista = ""
last_updated = 1598534304.6135302
update_threshold = 3600

shee = {}
sheets_last_updated = 1598534304.6135302
sheets_update_threshold = 3600

ksyk_url = "https://ksyk.fi"
sheets_url = "https://docs.google.com/spreadsheets/d/1dxvJz33F-LT71VYN5d97AhJ5FbpU9Sqlhf_TwS4k-bM"

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
def getSheets(s_id, s_key):
    global sheets_url
    try:
        sheets_url = os.environ['sheets_url']
    except Exception as e:
        print("\"sheets_url\" not set as an environ, the default url \"" + sheets_url + "\" will be used.")
    sheets = Sheets.from_developer_key(s_key)
    s = sheets.get(sheets_url)
    print("Sheet loaded: " + str(s))
    return s
def updateSheets():
    global use_sheets, shee
    print("Updating sheets data...")
    s_key = "";
    s_id = "";
    try:
        s_key = os.environ['secret_key']
    except Exception as e:
        print("\"secret_key\" not set as an environ, google sheets will be unavaible.")
        use_sheets = False
    try:
        s_id = os.environ['secret_id']
    except Exception as e:
        print("\"secret_id\" not set as an environ, google sheets will be unavaible.")
        use_sheets = False
    u_s = use_sheets
    if use_sheets:
        try:
            shee = getSheets(s_id, s_key)
            u_s = True
        except Exception as e:
            print("Sheets could not be loaded, please confirm that the url is correct and you have the rights to use it. \nError: "+ str(e))
            u_s = False
    print("Updated sheets data.")
    return u_s
last_u_s = False
def check_sheets_update():
    global sheets_last_updated, last_u_s
    now = time.time()
    diff = -(sheets_last_updated - now)
    if diff > sheets_update_threshold:
        last_u_s = updateSheets()
        sheets_last_updated = now
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
    return jsonify({'menu':ruokalista, 'recent_query_count':c, 'menu_time_since_last_update' : idle, 'menu_last_updated' : last_updated, 'menu_source_site':ksyk_url, 'menu_update_threshold':update_threshold, 'sheets_enabled':u_s, 'sheet_docs_name': str(shee), 'sheets_last_updated':sheets_last_updated, 'sheets_update_threshold':sheets_update_threshold, 'sheets_time_since_last_update':(sheets_last_updated - now())*-1}), 200
if __name__ == '__main__':
    updateData()
    updateSheets()
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)