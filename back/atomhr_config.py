from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import datetime

# Flask etc
app = Flask(__name__)
app.config['DEBUG'] = True
# app.config['DEBUG'] = False
app.config["JWT_SECRET_KEY"] = "secretkey"
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 36000

cors = CORS(app)
jwt = JWTManager(app)

url_base = '/atom/api/'
