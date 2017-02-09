import cgi
import datetime
import webapp2
from collections import OrderedDict

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import urlfetch

import os
import jinja2
import urllib, hashlib
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__).split('/')[:-1])),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)


def setTemplate(self, template_values, templateFile):
    _templateFolder = 'templates/'
    # add Defaults
    template_values['_templateFolder'] = _templateFolder
    template_values['_year'] = str(datetime.datetime.now().year)


    path = os.path.normpath(_templateFolder+templateFile)
    print(path)
    template = JINJA_ENVIRONMENT.get_template(path)
    self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):
    def get(self, mailSent=False):
        setTemplate(self, {"indexPage": True, 'mailSent': mailSent}, 'index.html')
        # data = {'mailSent':mailSent}
        # setTemplate(self, data, 'index.html')

    def post(self):
        email   = self.request.get('email')
        name    = self.request.get('name')
        message = self.request.get('message')

        sender_address = "DISC Mail <lindseyheagy@gmail.com>"
        email_to = ["Lindsey Heagy <lindseyheagy@gmail.com>"]
        email_subject = "DISC2017 Mail"
        email_message = "New email from:\n\n%s<%s>\n\n\n%s\n" % (name, email, message)

        mail.send_mail(sender_address, email_to, email_subject, email_message)
        self.get(mailSent=True)


class Schedule(webapp2.RequestHandler):

    @property
    def where(self):
        if getattr(self, '_where', None) is None:
            self.__class__._where = json.load(
                open('./templates/where/where.json', 'r'),
                object_pairs_hook=OrderedDict
            )
        return self._where


    def get(self):
        setTemplate(self, {'where':self.where}, 'schedule.html')


class Events(webapp2.RequestHandler):

    def get(self):
        setTemplate(self, {}, 'events.html')
        # data = {'mailSent':mailSent}
        # setTemplate(self, data, 'index.html')


class Images(webapp2.RequestHandler):
    def get(self):
        self.redirect('http://disc2017.geosci.xyz'+self.request.path)


class Assets(webapp2.RequestHandler):
    def get(self):
        self.redirect('http://disc2017.geosci.xyz'+self.request.path)


class Where(webapp2.RequestHandler):

    @property
    def where(self):
        if getattr(self, '_where', None) is None:
            self.__class__._where = json.load(
                open('./templates/where/where.json', 'r')
            )
        return self._where

    def get(self):
        loc = self.request.path.split('/')[-1]
        # where = [w.rsplit('.')[0] for w in os.listdir('./templates/where/')]
        # where = json.load(open('./templates/where/where.json', 'r'))


        if loc in self.where.keys():
            args = self.where[loc]
            args['name'] = loc
            setTemplate(self, args, 'where/template.html')
        else:
            setTemplate(self, {}, 'error.html')


where = json.load(open('./templates/where/where.json', 'r'))
print('|'.join(where.keys()))
base_apps = [
    ('/', MainPage),
    # ('/({})'.format('|'.join(where.keys())), Where),
    ('/events', Events),
    ('/assets', Assets),
    ('/schedule', Schedule),
    ('/img/.*', Images),
    ('/.*', Where)
]

app = webapp2.WSGIApplication(
    base_apps, debug=os.environ.get("SERVER_SOFTWARE", "").startswith("Dev")
)
