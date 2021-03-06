from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import traceback
import data
import json
import requests
import tempfile
app = Flask(__name__)
#TODO: Add secret key

@app.route('/widgets/<path:filename>')
def base_static(filename):
    return send_from_directory(app.root_path + '/widgets/', filename)

from bs4 import BeautifulSoup
import re
currend = 0
@app.before_first_request
def init():
    global l
    global currend
    for i in range(currend,currend+100,10):
        url = "https://www.google.com/search?q='covid'+'testing'+'sites'+'new'+'open'&tbl=qdr:d&tmb=nws&start="+str(i)
        browser = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':browser,}
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")
        for link in soup.find_all('a'):
            if(link.get('href')[0:4]=="/url"):
                l.append("https://google.com"+link.get('href'))
        print(l)
    currend = currend + 100
l = []
inc = -1

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/index.html')
def home2():
    return render_template("index.html")

@app.route('/curr.html')
def map():
    return render_template("curr.html")

@app.route('/crowd.html', methods=["GET","POST"])
def crowd():
    global l
    global inc
    inc += 1
    if(inc>=currend):
        init()
    if(request.method=="POST"):
        try:
            name = request.form["name"]
            coords = request.form["coords"]
            try:
                check = request.form["check"]
                inc = inc - 1
            except:
                pass
            coordsformatted = [float(i) for i in coords.split(",")][::-1]
            info = request.form["info"]
            geojson = {
                "markers": [], "type": "FeatureCollection", "properties": {}, "groups": [],
                "features": [
            {
                "type" : "Feature",
                "geometry" : {
                    "type" : "Point",
                    "coordinates" : coordsformatted
                },
                "properties" : {
                    "title" : name.encode("utf-8"),
                    "description" : info.encode("utf-8")
                }
            }
            ]
            }

            url = 'https://maphub.net/api/1/map/append'

            api_key = 'YWO4wwxjn2B8t6C8'

            args = {
                'file_type': 'geojson',
                'map_id' : 90293
            }

            headers = {
                'Authorization': 'Token ' + api_key,
                'MapHub-API-Arg': json.dumps(args)
            }

            tempname = None

            with tempfile.NamedTemporaryFile(delete=False) as fil:
                fil.write(json.dumps(geojson))
                tempname=fil.name

            with open(tempname, "r") as fil:
                r = requests.post(url, headers=headers, data=fil)
            newlist = [x.encode() for x in r.json().keys()]
            if('error' not in newlist):
                name=request.form["id"]
                data.register(name)
                data.giveUserPoints(name, 5)
                data.userAdded(name)
        except Exception:
            pass
    return render_template("crowd.html", link=l[inc])

@app.route('/lead.html')
def lead():
    mydict = {k: {k1.encode("utf-8"): v1 for k1, v1 in v.iteritems()} for k,v in data.getUsers()[0].iteritems()}
    return render_template("lead.html", peeps=mydict)

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    not_started = False
            except:
                time.sleep(2)

def run():
    from webapp import app
    start_runner()
    app.run(debug=True, use_reloader=False)
