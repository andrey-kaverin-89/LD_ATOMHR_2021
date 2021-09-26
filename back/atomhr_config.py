from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from speechpro.cloud.speech.recognition import RecognitionClient
from speechpro.cloud.speech.recognition import enums

import datetime
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# CRT
username = "////////////" # Please enter your creds to speech kit
password = "////////////" # Please enter your creds to speech kit
domain_id = 42 # Please enter your creds to speech kit
client = RecognitionClient(username, domain_id, password)
config = {
    'language': enums.Language.RU,
    'model': enums.Model.GENERAL,
    'encoding': enums.AudioEncoding.OGG_OPUS,
    'response_type': enums.ResponseType.PLAIN_TEXT
}

# Flask etc
app = Flask(__name__)
app.config['DEBUG'] = True
# app.config['DEBUG'] = False
app.config["JWT_SECRET_KEY"] = "secretkey"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/atom_test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name' # change to real mysql creds
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 36000

cors = CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

url_base = '/atom/api/'