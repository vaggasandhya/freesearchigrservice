# !/usr/bin/env python
# coding: utf-8

import numpy as np
import datetime
import flask
import json
import base64
import time
import io
import os
import random
from threading import Thread
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import Flask, render_template, request, redirect, url_for, abort, flash, jsonify, make_response
from PIL import Image
from werkzeug.utils import secure_filename
# from pdf2image import convert_from_path
from statistics import mode
from functools import wraps
from multiprocessing import Process, Pool, cpu_count
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                get_raw_jwt)

import PIL.Image

PIL.Image.MAX_IMAGE_PIXELS = None

# Initialize Flask app and Keras

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True

app.config['JWT_SECRET_KEY'] = 'kldLaDFI7584%38&mFyt&84cvT593(jfkdJkg@1'
jwt = JWTManager(app)

username = "MLlearningUser"
password = "sandhya@1234!"

global model

with open('config.json','r') as f:
    jdata = json.load(f)


@app.route("/details", methods=["POST"])
@jwt_required

def predict():
    json_data = json.loads(flask.request.data.decode('utf-8'))
    print(json_data)
    registration_type = json_data['registration_type']
    district= json_data['district']
    sro = json_data['sro']
    year= json_data['year']
    doc_no = json_data['doc_no']
    start_time = datetime.datetime.utcnow()
    print(start_time)
    from captcha import scan
    scan(registration_type =registration_type,district=district,sro=sro,year=year,doc_no=doc_no)
    return flask.jsonify(jdata)




# step1 : creating the Token
@app.route("/login", methods=["POST"])
def login():
    request_data = json.loads(flask.request.data.decode('utf-8'))
    response = {}
    status_code = 401

    u_name = request_data.get('username', '')
    u_password = request_data.get('password', '')
    if not u_name or not u_password:
        response = {'msg': 'Username & Password both are required'}
        status_code = 400

    elif u_name == username and u_password == password:
        access_token = create_access_token(identity=u_name,
                                           expires_delta=datetime.timedelta(days=36500))
        print(f'access_token is: {access_token}')
        response = {'token': access_token, 'msg': 'Login successful'}
        status_code = 200

    elif u_name != username or u_password != password:
        response = {'msg': 'Invalid credentials'}

    response = make_response(jsonify(response), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


# Start the server
if __name__ == "__main__":
    print(("* Loading Flask starting server..."
           "please wait until server has fully started"))
    app.run()
