from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.escape import json_encode
from tornado.gen import coroutine
from tornado.options import define, options

import jwt
import json
import requests
import os, uuid, sys
from motor import MotorClient
from passlib.hash import pbkdf2_sha256
from datetime import datetime


def get_token(email_id, time):
    return jwt.encode({"email_id" : email_id, "time" : time}, secret, algorithm = 'HS256')

db = MotorClient('mongodb://cse325user:cse325pass@ds157390.mlab.com:57390/cse325')['cse325']
secret = 'secret_key_goes_here'
