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
import webapp2
import jinja2
import os
import logging
from datetime import datetime
from google.appengine.ext import db

class Meeting(db.Model):
  place = db.StringProperty()
  place_url = db.LinkProperty()
  start_at = db.DateTimeProperty(required=True)
  duration = db.StringProperty()
  session_number = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):
  def get(self):
    current_meeting = Meeting.all().get()
    if not current_meeting:
      current_meeting = set_default_meeting()

    template_values = get_meeting_value(current_meeting)
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class AdminHandler(webapp2.RequestHandler):
  def get(self):
    current_meeting = Meeting.all().get()
    if not current_meeting:
      current_meeting = set_default_meeting()

    template_values = get_meeting_value(current_meeting)
    template = jinja_environment.get_template('datepicker.html')
    self.response.out.write(template.render(template_values))


class MeetingHandler(webapp2.RequestHandler):
  def post(self):
    current_meeting = Meeting.all().get()
    if not current_meeting:
      current_meeting = set_default_meeting()
    current_meeting.place = self.request.get('place')
    current_meeting.place_url = self.request.get('place_url')
    current_meeting.duration = self.request.get('duration')
    current_meeting.session_number = int(self.request.get('session_number'))
    s = self.request.get('start_at')
    fmt = '%Y-%m-%d'
    current_meeting.start_at = datetime.strptime(s, fmt)
    current_meeting.put()

    self.redirect('/')


def get_meeting_value(meeting):
  # t.strftime('%Y-%m-%d %H:%M:%S')
  return {'start_at': meeting.start_at.strftime('%Y-%m-%d'),
          'place': meeting.place,
          'place_url': meeting.place_url,
          'duration': meeting.duration,
          'session_number': meeting.session_number}


def set_default_meeting():
  meeting = Meeting(start_at=datetime.now())
  meeting.place = "unknown"
  meeting.place_url = "http://www.google.com/"
  meeting.duration = 'unknown'
  meeting.session_number = 0
  meeting.put()
  return meeting



app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/admin711', AdminHandler),
                               ('/meeting', MeetingHandler)],
                              debug=True)
