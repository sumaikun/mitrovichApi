import requests
import json
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from modules.app import app, mongo, flask_bcrypt, jwt
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import datetime

@app.route('/readOrderCreationFromHooks', methods=['POST'])
def readOrderCreationFromHooks():

    jsonData = request.get_json()

    #print("data",data["id"])

    shippingMethod = None

    data = {}

    for line in jsonData["shipping_lines"]:
        #print("line",line)
        if line["method_id"] == "mitrovich":
            shippingMethod = "international"
            data["shippingValue"] = line["total"]
            data["shippingMethod"] = shippingMethod

    if shippingMethod is None:
         return jsonify({'message': 'mitrovich won´t send this shipping'}), 200
    else :

        shipping = jsonData["shipping"]

        data["createdAt"] = datetime.datetime.utcnow()
        data["shopDate"] = jsonData["date_created"]
        data["shopID"] = jsonData["id"]
        data["country"] = shipping["country"]
        data["state"] = shipping["state"]
        data["city"] = shipping["city"]
        data["address"] = shipping["address_1"]
        data["postalCode"] = shipping["postcode"]
        data["name"] = shipping["first_name"] + shipping["last_name"] 

        productsDetail = {}

        data["product"] = []

        for line in jsonData["line_items"]:
            productsDetail["name"] = line["name"]
            productsDetail["quantity"] = str(line["quantity"]) 
            productsDetail["product_id"] = str(line["product_id"]) 
            productsDetail["variation_id"] = str(line["variation_id"])
            productsDetail["price"] = str(line["price"])  
            data["product"].append(productsDetail)
        
        data["shop"] = "testing Shop"

        print("data",data)
       
        #result = mongo.db.mitrovich_shippings.insert_one(data)

        return jsonify({'message': 'order creation readed'}), 200

    #return jsonify({'message': 'message received'}), 200

@app.route('/ecommerceShippings', methods=['GET'], endpoint='ecommerceShippings')
@jwt_required()
def ecommerceShippings():
    if request.method == 'GET':
        
        #query = request.args
        data = json.loads(dumps(mongo.db.mitrovich_shippings.aggregate([
            {'$addFields': {"_id": { '$toString':'$_id'}}}
        ])))
        #print("data",data)
        #print("len",len(data))
        return jsonify(data), 200

