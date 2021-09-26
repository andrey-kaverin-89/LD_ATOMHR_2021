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
# Text to params
import spacy
from spacy import displacy

# A-2 imports
import atomhr_orm as orm
from atomhr_config import app, cors, db, jwt, url_base, client, config, morph

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

# Get voice to params
@app.route(url_base+'v1/voice',  methods=['POST'])
# Using for DEBUGGING. Uncomment below.
# @jwt_required()
def get_prediction():
    try:
        content = request.files['src'].read()
        text = client.recognize(config, content).text
        nlp = spacy.load("ru_core_news_sm")
        doc = nlp(text)
        # Get Data from base
        df = pd.DataFrame([x.serialize for x in orm.Employee.query.all()])
        # Some magic with data
        df.marital_status = df.marital_status.replace(
            {
                "Разв.": "развод", 
                "Жен/ЗМ": "женат/замужем", 
                "Вдов.": "вдова/вдовец",
                "ГрБрак": "гражданский брак",
                "Хол/НЗ": "свободен/свободна"
            }
        )
        cat_columns = ["position", "gender", "marital_status", "absence", "city",]
        unique_cat_values = []
        for col in cat_columns:
            unique_cat_values.extend(df[col].unique())
        df.absence = df.absence.replace({"Прочие отсутствия ": "другие причины"})g
        unique_cat_values = (" ".join(token.lower() for token in unique_cat_values if token is not np.nan)).split(" ")
        unique_cat_values_normed = [morph.parse(token)[0].normal_form for token in unique_cat_values]
        columns = ["id", "Должность", "Пол", "Семейное положение", "Причина отсутствия", "Количество дней отсутсвия", "Зарплата", "Город", "Количество детей", "Возраст", "Был наставник", "Опыт работы", "Месяц трудоустройства", "Месяц увольнения", "Многодетная семья", "На пенсии",]
        normed_columns = [morph.parse(token)[0].normal_form for token in columns]
        df.columns = columns
        # Key words
        comparison_words = {
            "greater": ["старший", "большой"],
            "smaller": ["младший", "молодой", "маленький"],
            "equals": ["равно", "равный"]
        }
        # Starting to parse
        out = Entities()
        measures = None
        for token in doc:
            normed = morph.parse(token.text)[0].normal_form
            if len(normed) < 2:
                continue
            if normed in ["средний", "максимальный", "минимальный"]:
                measures = normed
                continue                
            if token.dep_ in ["obj", "conj", "obl", "nsubj", "nmod"]:
                for norm_col, col in zip(normed_columns, columns):
                    dist = damerau_levenshtein_distance(normed, norm_col)
                    if dist < 3 or normed + " " in norm_col:
                        value = find_in_children(token, unique_cat_values_normed)
                        out.append(Entity(table_name=col, original_name=token.text, comparison="=", value=value))            
            for comp in comparison_words:
                if normed in comparison_words[comp]:
                    if len(out.get_entities_list()) > 0:
                        out[out.get_entities_list()[-1]].comparison = comp
            if token.dep_ in ["nummod", "appos", "punct"]:
                if len(out.get_entities_list()) > 0:
                    out[out.get_entities_list()[-1]].value = token.textres = []
        # Save result
        res = []
        for i in out.get_entities_list():
            filters = {}
            filters["member"] = out[i].table_name
            filters["operator"] = out[i].comparison
            filters["values"] = out[i].value
            res.append(filters)
        return jsonify(result = {'measures': measures, 'filters': res},
                    action = 'get_prediction',
                    status='ok'), 200
    # for DEBUGGING
    # except Exception as e:
        # return jsonify(result = {'error':e},
    except:
        return jsonify(result = {'error':'something went wrong'},
                       action = 'get_prediction',
                       status='error'), 500

# Additional functions and classes

# Levi func
def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in range(-1,lenstr2+1):
        d[(-1,j)] = j+1
 
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + 1) # transposition
 
    return d[lenstr1-1,lenstr2-1]

# Single entity for filter
class Entity(object):
    def __init__(self, table_name, original_name, comparison, value):
        self.table_name = table_name
        self.comparison = comparison
        self.value = value
        
        self.original_name = original_name
    
    def __str__(self):
        return f"Column: {self.table_name}, comparison: {self.comparison}, value: {self.value}"

# Detect entities
class Entities(object):
    def __init__(self):
        self.entities = []
        
    def __getitem__(self, name):
        for ent in self.entities:
            if ent.table_name == name:
                return ent
    
    def __len__(self):
        return len(self.entities)
            
    def get_by_original_name(self, name):
        for ent in self.entities:
            if ent.original_name == name:
                return ent
        return
    
    def append(self, entity):
        self.entities.append(entity)        
        
    def get_entities_list(self):
        return [entity.table_name for entity in self.entities]
    
    def original_names_list(self):
        return [entity.original_name for entity in self.entities]

# Recurent tokenizer
def find_in_children(token, unique_cat_values_normed):
    res = []
    for child in token.children:
        res.append(child)
        for ch in child.children:
            res.append(ch)
    for i in res:
        normed = morph.parse(i.text)[0].normal_form
        if normed in unique_cat_values_normed:
            return normed
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')