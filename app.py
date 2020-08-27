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

app = Flask(__name__)

c = 0

version = 1

ruokalista = ""
last_updated = 1598534304.6135302
update_threshold = 3600/3

ksyk_url = "https://ksyk.fi"

def getMenu():
    page = urlopen(ksyk_url).read()
    soup = BeautifulSoup(page,features="lxml")
    matches = soup.find_all("div", class_="et_pb_tab_content")[0]
    children = matches.findChildren("p" , recursive=False)
#    print(children)
    return str(children[0].get_text(" \n "))
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
    return jsonify({'menu':ruokalista, 'recent_query_count':c, 'idle_time_before_this' : idle, 'last_updated' : last_updated}), 200
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    updateData()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)