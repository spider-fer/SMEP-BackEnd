from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId
from datetime import datetime

db = client.smep
location_collection = db.locations

fecha = datetime.now()
fecha_string = fecha.strftime("%d/%m/%Y")

@app.route('/locations', methods=['POST'])
def createLocation():
    if location_collection.find_one({"nombre": {"$eq": request.json['nombre']}}):
        return jsonify({"msg": 'Location with that name already exists'})
    else:
        id = location_collection.insert_one({
            'nombre':request.json['nombre'],
            'idsupervisor':"null",
            'fecharegistro':fecha_string,
            'horariosinfo': request.json['horariosinfo'],
        }).inserted_id
        return jsonify(str(id))

@app.route('/locations', methods=['GET'])
def getLocations():
    locations =[]
    for doc in location_collection.find():
        locations.append({
            '_id': str(ObjectId(doc['_id'])),
            'nombre':doc['nombre'],
            'idsupervisor':doc['idsupervisor'],
            'fecharegistro':doc['fecharegistro'],
            'horariosinfo': doc['horariosinfo'],
        })
    return (locations)

@app.route('/location/<id>', methods=['GET'])
def getLocation(id):
    location = location_collection.find_one({'_id':ObjectId(id)})
    print(location)
    return jsonify({
        '_id': str(ObjectId(location['_id'])),
        'nombre':location['nombre'],
        'idsupervisor':location['idsupervisor'],
        'fecharegistro':location['fecharegistro'],
        'horariosinfo': location['horariosinfo'],
    })

@app.route('/location/<id>', methods=['DELETE'])
def deleteLocation(id):
    location_collection.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg": 'Location deleted'})

@app.route('/location/<id>', methods=['PUT'])
def updateLocation(id):
    location_collection.update_one({'_id':ObjectId(id)}, {'$set':{
        'nombre':request.json['nombre'],
        'idsupervisor':request.json['idsupervisor'],
        'fecharegistro':fecha_string,
        'horariosinfo': request.json['horariosinfo'],
    }})
    return jsonify({"msg": 'Location updated'})

if __name__ == "__main__":
    app.run(debug=True)