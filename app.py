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

c = 0

version = 1

ruokalista = ""
last_updated = 1598534304.6135302
update_threshold = 3600

ksyk_url = "https://ksyk.fi"

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
def getUID(ip):
    return hashlib.sha256(str(ip).encode("utf8")).hexdigest()

@app.route('/')
def hello():
    global chat, version
    uIp = request.access_route[0]
    uID = getUID(uIp)
    global c
    c = c + 1
    idle = updateData()
    s_key = "";
    try:
        s_key = os.environ['secret_key']
    except Exception as e:
        print("\"secret_key\" not set as an environ, google sheets will be unavaible.")
    return jsonify({'menu':ruokalista, 'recent_query_count':c, 'time_since_last_update' : idle, 'last_updated' : last_updated, 'source_site':ksyk_url, 'update_threshold':update_threshold, 'secret_key_test': s_key}), 200
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    updateData()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)