from google.appengine.ext import db

class Date(db.Model):
	datepicked = db.DateProperty(required=True)
	
	date = db.DateTimeProperty(auto_now_add=True)
    
