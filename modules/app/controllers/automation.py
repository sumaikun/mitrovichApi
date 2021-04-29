import requests
import json
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from modules.app import app, mongo, flask_bcrypt, jwt
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import datetime
from modules.app.automations.servientrega import servientrega_automation
from modules.app.automations.pesos import pesos_automation

@app.route('/servientregaReport', methods=['POST'], endpoint='servientregaReport')
@jwt_required()
def servientregaReport():
    if request.method == 'POST':
        
        jsonData = request.get_json()

        automation = servientrega_automation()

        automation.start_script()

        return jsonify({'message': 'proccess fired'}), 200

@app.route('/getCurrentPesosValue', methods=['POST'], endpoint='getCurrentPesosValue')
def getCurrentPesosValue():
    if request.method == 'POST':
        
        jsonData = request.get_json()

        automation = pesos_automation()

        value = automation.start_script()

        return jsonify({'message': 'proccess fired','value':value }), 200

