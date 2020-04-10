import pyrebase
from dotenv import load_dotenv
import os

config = {
    "apiKey": os.getenv('API'),
    "authDomain": "crowdcovid.firebaseapp.com",
    "databaseURL": "https://crowdcovid.firebaseio.com",
    "projectId": "crowdcovid",
    "storageBucket": "crowdcovid.appspot.com",
    "messagingSenderId": "890555948483",
    "appId": "1:890555948483:web:e8fc491ed6713cae327176"
}

# Firebase initialization
firebase = pyrebase.initialize_app(config)
#auth = firebase.auth()
#user = auth.sign_in_with_email_and_password("21qinw@millburn.org", os.getenv("PASS"))
#user = auth.refresh(user['refreshToken'])
db = firebase.database()

def register(user):
    """Adds a user to the database."""
    if(db.child("Users").child(user).get().val()==None):
        db.child("Users").child(user).set({"points":0,"additions":0,"validations":0})

def getItems(products):
    """Returns the products appropriately type-casted."""
    return [dict((product.key(), product.val()) for product in products)] if products is not None else [{}]

def getUsers():
    """Gets all the users."""
    return getItems(db.child("Users").get().each())

def giveUserPoints(name, points):
    points = points + db.child("Users").child(name).get().val()["points"]
    db.child("Users").child(name).update({"points":points})

def userAdded(name):
    points = 1 + db.child("Users").child(name).get().val()["additions"]
    db.child("Users").child(name).update({"additions":points})
