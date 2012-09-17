#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import os
from dbmodel import *
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import datetime

admin_list = ['chaoju.huang@gmail.com', 'leoleo168@gmail.com', 'nick90225@gmail.com']

class MainPage(webapp.RequestHandler):
    def get(self):
        date_picked = Date.all().get()
        if date_picked:
            template_values = {'date': str(date_picked.datepicked).split('-'), 
                               'place': date_picked.place,
                               'place_url': date_picked.place_url,
                               'time': date_picked.time,
                               'round': date_picked.round}
        else:
            template_values = {'date': ['00', '00', '00']}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class Admin(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if True:
            date_picked = Date.all().get()
            template_values = {'round': date_picked.round,
                               'logout_uri': users.create_logout_url('/')}
            path = os.path.join(os.path.dirname(__file__), 'datepicker.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_logout_url('/'))  
        
class SetDate(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if True:
            self.renew_date()
        else:
            self.redirect(users.create_logout_url('/'))
    
    def renew_date(self):
        try:
            date_str = self.request.get('date')
            date_str = date_str.split('/')
            date_str = date_str[-1:] + date_str[:-1]
            
            if self.request.get('date'):
                if Date.all().count() < 1:
                    date_picked = Date(datepicked=datetime.date(*[int(s) for s in date_str]))
                    date_picked.place = self.request.get('place')
                    date_picked.place_url = self.request.get('place_url')
                    date_picked.time = self.request.get('time')
                    date_picked.round = self.request.get('round')
                    date_picked.put()
                else:
                    date_picked = Date.all().get()
                    date_picked.datepicked = datetime.date(*[int(s) for s in date_str])
                    date_picked.place = self.request.get('place')
                    date_picked.place_url = self.request.get('place_url')
                    date_picked.time = self.request.get('time')
                    date_picked.round = self.request.get('round')
                    date_picked.put()
                    
                template_values = {'status': 'ok',
                                   'date': date_picked.datepicked,
                                   'place': date_picked.place,
                                   'place_url': date_picked.place_url,
                                   'time': date_picked.time,
                                   'round': date_picked.round,
                                   'logout_uri': users.create_logout_url('/')}
            else:
                template_values = {'status': 'error'}
            
        except ValueError:
            template_values = {'status': 'error'}
        
        path = os.path.join(os.path.dirname(__file__), 'datepicker.html')
        self.response.out.write(template.render(path, template_values))

        self.redirect('/')

class ODYCPAA2012IndexHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'odycpaa2012index.html')
        self.response.out.write(template.render(path, template_values))

class ODYCPAA2012RulesHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'odycpaa2012rules.html')
        self.response.out.write(template.render(path, template_values))
        
class NotFoundPageHandler(webapp.RequestHandler):
    def get(self):
        self.error(404)
        self.response.out.write('<h1>Uh oh! (404 Error)</h1>')           

application = webapp.WSGIApplication([('/', MainPage),
	                                  ('/admin711', Admin),
                                      ('/set_date', SetDate),
                                      ('/flasjkdflwkejrhla', ODYCPAA2012IndexHandler),
                                      ('/aslzxkcuvhaawelkr', ODYCPAA2012RulesHandler),
                                      ('/.*', NotFoundPageHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
