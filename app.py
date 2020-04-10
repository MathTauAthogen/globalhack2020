from flask import Flask, render_template, request
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

peeps={"00001":{"name":"William Qin", "score":100, "add":5, "check":5}} #TODO: Get from database

@app.route('/lead.html')
def lead():
    return render_template("lead.html", peeps=peeps)

@app.route('/api/addplace', methods=["POST"])
def add():
    print(request.form)
    name = request.form["name"]
    coords = request.form["coords"]
    print(coords)
    coordsformatted = map(int,coords.split(","))
    info = request.form["info"]
    geojson = {
        "type" : "Feature",
        "geometry" : {
            "type" : "Point",
            "coordinates" : coordsformatted
        },
        "properties" : {
            "title" : name,
            "description" : info
        }
    }
    print(geojson)
    return render_template("crowd.html")
