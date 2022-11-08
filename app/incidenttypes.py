from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId

db = client.smep
incidenttype_collection = db.incidenttypes

@app.route('/incidenttypes', methods=['POST'])
def createIncidentType():
    id = incidenttype_collection.insert_one({
        'nombre':request.json['nombre'],
        'descripcion':request.json['descripcion'],
        'imgdescrip':request.json['imgdescrip']
    }).inserted_id
    return jsonify(str(id))

@app.route('/incidenttypes', methods=['GET'])
def getIncidentTypes():
    incidenttypes =[]
    for doc in incidenttype_collection.find():
        incidenttypes.append({
            '_id': str(ObjectId(doc['_id'])),
            'nombre':doc['nombre'],
            'descripcion':doc['descripcion'],
            'imgdescrip':doc['imgdescrip']
        })
    return (incidenttypes)

@app.route('/incidenttype/<id>', methods=['GET'])
def getIncidentType(id):
    incidenttype = incidenttype_collection.find_one({'_id':ObjectId(id)})
    print(incidenttype)
    return jsonify({
            '_id': str(ObjectId(incidenttype['_id'])),
            'nombre':incidenttype['nombre'],
            'descripcion':incidenttype['descripcion'],
            'imgdescrip':incidenttype['imgdescrip']
    })

@app.route('/incidenttype/<id>', methods=['DELETE'])
def deleteIncidentType(id):
    incidenttype_collection.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg": 'Incident Type deleted'})

@app.route('/incidenttype/<id>', methods=['PUT'])
def updateIncidentType(id):
    incidenttype_collection.update_one({'_id':ObjectId(id)}, {'$set':{
        'nombre':request.json['nombre'],
        'descripcion':request.json['descripcion'],
        'imgdescrip':request.json['imgdescrip']
    }})
    return jsonify({"msg": 'Incident Type updated'})

if __name__ == "__main__":
    app.run(debug=True)