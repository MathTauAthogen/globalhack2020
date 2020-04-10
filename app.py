from flask import Flask, render_template, request
import json
import requests
import tempfile
app = Flask(__name__)
#TODO: Add secret key

from bs4 import BeautifulSoup
import re
@app.before_first_request
def init():
    global l
    for i in range(0,100,10):
        url = "https://www.google.com/search?q='covid'+'testing'+'sites'+'open'&start="+str(i)
        browser = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':browser,}
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")
        links = soup.findAll("a")
        for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            l.append(re.split(":(?=http)",link["href"].replace("/url?q=",""))[0])
    print(l)


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

@app.route('/crowd.html')
def crowd():
    global l
    global inc
    inc += 1
    print(l)
    return render_template("crowd.html", link=l[inc])

peeps={"00001":{"name":"wqin2008@gmail.com", "score":100, "add":5, "check":5}} #TODO: Get from database

@app.route('/lead.html')
def lead():
    return render_template("lead.html", peeps=peeps)

@app.route('/addplace', methods=["POST"])
def add():
    name = request.form["name"]
    coords = request.form["coords"]
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

    return render_template("crowd.html")

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

def run():
    from webapp import app
    start_runner()
    app.run(debug=True, use_reloader=False)
