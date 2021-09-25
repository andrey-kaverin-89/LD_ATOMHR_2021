# Universal imports
import requests, json, time, datetime, re, hashlib, pickle
import pandas as pd, numpy as np
# Sklearn import for feature importances
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report
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

# Ping
@app.route(url_base+'v1/ping',  methods=['GET'])
def ping():
    return 'pong'

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
        dset = pd.read_excel(request.files.get('file', None), sheet_name='1', skiprows=2, index_col='id')
        # To database
        for i in range(len(dset)):
            db.session.add(orm.Employee(position        = dset.iloc[i]['position'],
                                        gender          = dset.iloc[i]['gender'],
                                        marital_status  = dset.iloc[i]['marital_status'],
                                        job_stop        = dset.iloc[i]['job_stop'],
                                        absence         = dset.iloc[i]['absence'],
                                        absence_days    = dset.iloc[i]['absence_days'],
                                        salary          = dset.iloc[i]['salary'],
                                        city            = dset.iloc[i]['city'],
                                        children_num    = dset.iloc[i]['children_num'],
                                        age             = dset.iloc[i]['age'],
                                        has_mentor      = dset.iloc[i]['has_mentor'],
                                        experience      = dset.iloc[i]['experience'],
                                        job_start_month = dset.iloc[i]['job_start_month'],
                                        layoff_month    = dset.iloc[i]['layoff_month'],
                                        is_large_family = dset.iloc[i]['is_large_family'],
                                        is_retiree      = dset.iloc[i]['is_retiree']))
        db.session.commit()
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

# Get feature importances
@app.route(url_base+'v1/get_feature_importances',  methods=['GET'])
# Using for DEBUGGING. Uncomment below.
# @jwt_required()
def get_feature_importances():
    try:
        cols = request.json
        # Get data from database
        dset = pd.DataFrame([x.serialize for x in orm.Employee.query.all()])
        for elem in dset.columns:
            if elem not in cols:
                dset = dset.drop(columns=[elem])
        # Some data science magic with grid search and random forests
        RANDOM_STATE = 42
        rf_model = RandomForestClassifier(random_state=RANDOM_STATE, class_weight="balanced")
        params = {
            "n_estimators": [50, 70, 100, ],
            "max_depth": [5, 10, 15],
            "max_features": ["auto", "sqrt", "log2"],
            "criterion": ["gini", "entropy"]
        }
        model = GridSearchCV(rf_model, params, cv=5)
        model.fit(dset[[dset.columns[:-1]]], dset[[dset.columns[-1]]])
        # Get feature importances
        result = [{'feature_name':x[0], 'weight':x[1]} for x in zip(dset.columns, model.best_estimator_.feature_importances_)]
        return jsonify(result = {'columns':result},
                    action = 'get_feature_importances',
                    status='ok'), 200
    # for DEBUGGING
    # except Exception as e:
        # return jsonify(result = {'error':e},
    except:
        return jsonify(result = {'error':'something went wrong'},
                       action = 'get_feature_importances',
                       status='error'), 500

# Get prediction
@app.route(url_base+'v1/get_prediction',  methods=['GET'])
# Using for DEBUGGING. Uncomment below.
# @jwt_required()
def get_prediction():
    try:
        id_pred = request.json.get('id',None)
        # Get data from database
        dset = orm.Employee.query.filter(orm.Employee.id == id_pred).first()
        # Get prediction from model in pickle
        with open('SVC.pickle','rb') as f:
            model = pickle.loads(f.read())
        result = model.predict(pd.DataFrame(dset.serialize))
        return jsonify(result = {'chance':result},
                    action = 'get_prediction',
                    status='ok'), 200
    # for DEBUGGING
    # except Exception as e:
        # return jsonify(result = {'error':e},
    except:
        return jsonify(result = {'error':'something went wrong'},
                       action = 'get_prediction',
                       status='error'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
