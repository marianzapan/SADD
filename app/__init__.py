from flask import Flask, jsonify, url_for, request, flash
from werkzeug.routing import RequestRedirect
from json import dumps
import requests, gunicorn
app = Flask(__name__)

from datetime import timedelta
from flask_jwt_extended import JWTManager
app.config['JWT_SECRET_KEY'] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=5)
jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify(msg="El token expiró, debe iniciar sesión otra vez."), 401

app.secret_key = 'clave_de_sesion'
API_URL = "http://127.0.0.1:5000/api/"

def sendRequest(method, endpoint, token=None, data=None):
    if token: auth = { "Authorization" : "Bearer " + token }
    else: auth = None
    if data:
        if ('doc' in data): 
            if type(data['doc']) is bytes: data['doc'] = data['doc'].decode('utf-8')
            data['doc'] = str(data['doc'])
        if ('xml' in data):
            if type(data['xml']) is bytes: data['xml'] = data['xml'].decode('utf-8')
            data['xml'] = str(data['xml'])
        if ('pdf' in data):
            if type(data['pdf']) is bytes: data['pdf'] = data['pdf'].decode('utf-8')
            data['pdf'] = str(data['pdf'])
        if ('img' in data):
            if type(data['img']) is bytes: data['img'] = data['img'].decode('utf-8')
            data['img'] = str(data['img'])

    res = requests.request(method, API_URL+endpoint, headers=auth, data=dumps(data))
    if res.status_code == 401: raise RequestRedirect(url_for('login', expired=True)) #Token expired
    elif res.status_code == 403:
        if "?forbidden=True" in request.referrer: raise RequestRedirect(request.referrer)
        else: raise RequestRedirect(request.referrer + "?forbidden=True")
    elif res.status_code == 422: return 422
    else:
        res = res.json()
        if (type(res) is dict): res = [res]
        return res

from functools import wraps

def forbidden(func):
    @wraps(func)
    def forbidden_decorated_function(*args, **kwargs):
        forbidden = bool(request.args.get('forbidden'))
        if forbidden:
            flash("No tiene permiso para realizar esta acción.")
        return func(*args, **kwargs)
    return forbidden_decorated_function

def convertirBytes(B):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)

from app.api import getReadPermissions, chkPermissions

@app.context_processor
def utility_processor():
    def chkReadPermissions(usuario):
        return getReadPermissions(usuario)
    def chkAllPermissions(usuario, seccion, op):
        return chkPermissions(usuario, seccion, op)
    return dict(chkReadPermissions=chkReadPermissions, chkAllPermissions=chkAllPermissions)

from app import routes, api