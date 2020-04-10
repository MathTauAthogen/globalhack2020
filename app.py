from flask import Flask, render_template, request
import json
import requests
import tempfile
app = Flask(__name__)
#TODO: Add secret key

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
    return render_template("crowd.html")

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
    with open("test.json", "w+") as fil:
        fil.write(json.dumps(geojson))

    with open("test.json", "r") as fil:
        r = requests.post(url, headers=headers, data=fil)

    return render_template("crowd.html")
