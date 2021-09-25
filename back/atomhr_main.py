# Universal imports
import requests, json, time, datetime, re, hashlib
import pandas as pd, numpy as np

# Flask imports
from flask import request, jsonify, render_template, send_file
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request

# A-2 imports
import atomhr_orm as orm
from atomhr_config import app, cors, db, jwt, url_base

# CORS Headers
@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Auth-Token, Authorization'
    return response

# Auth endpoint
@app.route(url_base+'v1/auth',  methods=['POST'])
def auth():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # user_login = orm.User.query.filter(orm.User.email == username, orm.User.psw_hash == password).first_or_404()
    # access_token = create_access_token(identity=user_login.user_id)
    # Using for DEBUGGING. Uncomment above and comment below.
    access_token = create_access_token(identity=1)
    return jsonify(result = {'access_token':access_token},
                   action = 'auth',
                   status='ok'), 200

# Upload endpoint and response columns
@app.route(url_base+'v1/uploadfile',  methods=['POST'])
# Using for DEBUGGING. Uncomment below.
# @jwt_required()
def uploadfile():
    try:
        # Upload file from front-end
        dset = pd.read_excel(request.files.get('file', None), sheet_name='1', skiprows=2, index_col='ID')
        # Some magic...
        result = [{'name':x[0],'type':'num'} 
                if (x[1] == np.dtype('int')) or (x[1] == np.dtype('float'))
                else {'name':x[0],'type':'obj'} 
                for x in zip(dset.columns,dset.dtypes)]
        return jsonify(result = {'columns':result},
                    action = 'uploadfile',
                    status='ok'), 200
    # for DEBUGGING
    # except Exception as e:
        # return jsonify(result = {'error':e},
    except:
        return jsonify(result = {'error':'something went wrong'},
                       action = 'uploadfile',
                       status='error'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')