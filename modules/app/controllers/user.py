import os
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from modules.app import app, mongo, flask_bcrypt, jwt
from modules.app.models import validate_user, validate_login
import logger
from bson.objectid import ObjectId
import datetime
import json
from bson.json_util import dumps, loads
import boto3

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/users', methods=['GET', 'POST'], endpoint='users')
@jwt_required()
def users():
    if request.method == 'GET':
        
        #query = request.args
        data = json.loads(dumps(mongo.db.users.aggregate([
            {'$addFields': {"_id": { '$toString':'$_id'}}}
        ])))
        #print("data",data)
        #print("len",len(data))
        return jsonify(data), 200

    if request.method == 'POST':

        data = validate_user(request.get_json())
        if data['ok']:
            data = data['data']
            if 'password' in data:
                data['password'] = flask_bcrypt.generate_password_hash(
                    data['password'])
            data["createdAT"] = datetime.datetime.utcnow()
            result = mongo.db.users.insert_one(data)
            return jsonify({'message': 'User created successfully!','info':{'_id':result.inserted_id}}), 200
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400
            

@app.route('/users/<id>', methods=['GET', 'DELETE','PUT'],endpoint='user')
@jwt_required()
def user(id):
    
    #print("id",id)
    #print("args",request.args)

    if request.method == 'GET':
        data = mongo.db.users.find_one({"_id":ObjectId(id)})
        #print("data",data)       
        #print("len",len(data))
        
        """
        check = checkSimpleForeign("users",id)
        if check != True:
            return check
        """

        return jsonify(data), 200  
    if request.method == 'DELETE':
        db_response = mongo.db.users.delete_one({"_id":ObjectId(id)})
        if db_response.deleted_count == 1:
            response = {'message': 'record deleted'}
        else:
            response = {'message': 'no record found'}
        return jsonify(response), 200

    if request.method == 'PUT':
        #data = request.get_json()
        data = validate_user(request.get_json())
        if data['ok']:
            data = data['data']
            if 'password' in data:            
                data['password'] = flask_bcrypt.generate_password_hash(
                    data['password'])
            data["updatedAT"] = datetime.datetime.utcnow()        
            db_response = mongo.db.users.update_one({"_id":ObjectId(id)}, {'$set':data})
            #print("response",db_response.matched_count)
            if db_response.matched_count > 0:            
                return jsonify({'message': 'record updated'}), 200
            else:
                return jsonify({'message': 'error on record updated'}), 400   
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/auth', methods=['POST'])
def auth_user():
    ''' auth endpoint '''
    data = validate_login(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email': data['email']}, {"_id": 0})
        LOG.debug(user)
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            #refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            #user['refresh'] = refresh_token
            return jsonify(user), 200
        else:
            return jsonify({'message': 'invalid username or password'}), 401
    else:
        return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400
        

@app.route('/registerFirstUser', methods=['POST'])
def register():
    ''' register user endpoint '''
    users = len(json.loads(dumps(mongo.db.users.find())))
    #print("users",users)
    if users == 0:
        data = validate_user(request.get_json())
        if data['ok']:
            
            data = data['data']
            
            if data['password'] != None: 
                data['password'] = flask_bcrypt.generate_password_hash(
                    data['password'])
            data["createdAT"] = datetime.datetime.utcnow()            
            mongo.db.users.insert_one(data)
            return jsonify({'message': 'User created successfully!'}), 200
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400
    else:
        return jsonify({'message': 'can not created first user'}), 400