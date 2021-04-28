import requests
import json
import time
import pandas as pd
from flask import Flask, request, render_template
from Controller import DatabaseController
db = DatabaseController.SystemControl()


app = Flask(__name__)

@app.route('/api/v1/user', methods=['POST'])
def user_register_route():
    try:
        req = request.data.decode("utf-8")
        req = json.loads(req)
        req = dict(req)
    except:
        return 'Error: Cannot convert data into json!', 400
    result = db.user_register(req)
    return result.content, result.code
        
@app.route('/api/v1/user', methods=['GET'])
def user_get_route():
    try:
        req = request.data.decode("utf-8")
        req = json.loads(req)
        req = dict(req)
    except:
        return 'Error: Cannot convert data into json!', 400
    if not 'cpf' in req:
        return 'Error: Need a CPF to find a specific user.', 400
    result = db.user_get(req['cpf'])
    if result.code == 200:
        return json.dumps(result.content), 200
    else:
        return result.content, result.code

@app.route('/api/v1/debts', methods=['GET'])
def system_get_debts_route():
    result = db.debts_get()
    if result.code == 200:
        return json.dumps(list(result.content)), 200
    else:
        return result.content, result.code

@app.route('/api/v1/request/debt/pay', methods=['PUT'])
def system_request_pay():
    try:
        req = request.data.decode("utf-8")
        req = json.loads(req)
        req = dict(req)
    except:
        return 'Error: Cannot convert data into json!', 400
    if not 'cpf' in req:
        return 'Error: Need a CPF to find a specific user.', 400
    result = db.debts_update(req['cpf'])
    return result.content, result. code

if __name__ == '__main__':
    app.run(debug=True)