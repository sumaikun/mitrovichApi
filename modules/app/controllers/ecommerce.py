import requests
import json
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from modules.app import app, mongo, flask_bcrypt, jwt
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import datetime
from woocommerce import API

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

        shopUrl = jsonData["_links"]["self"][0]["href"].split("wp-json")[0]

        #print("shopUrl",shopUrl)

        shop = mongo.db.users.find_one({ 'shopUrl': {'$regex':shopUrl} })

        #print("shop",shop)

        if shop is None:
            return jsonify({'message': 'customer is not store on db'}), 200

        wcapi = API(
            url=shopUrl,
            consumer_key=shop["customerKey"],
            consumer_secret=shop["customerSecret"],
            timeout=50
        )
        
        data["shop"] = shopUrl

        shipping = jsonData["shipping"]
        billing = jsonData["billing"]

        data["createdAt"] = datetime.datetime.utcnow()
        data["shopDate"] = jsonData["date_created"]
        data["shopID"] = jsonData["id"]
        data["country"] = shipping["country"]
        data["state"] = shipping["state"]
        data["city"] = shipping["city"]
        data["address"] = [shipping["address_1"],shipping["address_2"]]
        data["postalCode"] = shipping["postcode"]
        data["name"] = shipping["first_name"] + " " + shipping["last_name"] 
        data["email"] = billing["email"] 
        data["phone"] = billing["phone"]
        productsDetail = {}

        data["product"] = []

        for line in jsonData["line_items"]:
            productsDetail["name"] = line["name"]
            productsDetail["quantity"] = str(line["quantity"]) 
            productsDetail["product_id"] = str(line["product_id"]) 
            ### get extra data from api
            response = wcapi.get('products/'+str(line["product_id"]))
            productApi = response.json()
            productsDetail["permalink"] = productApi["permalink"]
            productsDetail["dimensions"] = productApi["dimensions"]
            productsDetail["weight"] = productApi["weight"]
            productsDetail["variation_id"] = str(line["variation_id"])
            productsDetail["price"] = str(line["price"])  
            data["product"].append(productsDetail)
        
       

        #print("data",data)
       
        mongo.db.mitrovich_shippings.insert_one(data)

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

