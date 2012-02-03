from google.appengine.ext import db

class Date(db.Model):
    place = db.StringProperty()
    place_url = db.LinkProperty()
    datepicked = db.DateProperty(required=True)
    time = db.StringProperty()
    round = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
