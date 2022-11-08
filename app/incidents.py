from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId

db = client.smep
incident_collection = db.incidents

@app.route('/incidents', methods=['POST'])
def createIncident():
    id = incident_collection.insert_one({
        'idreservation':request.json['idreservation'],
        'iduser':request.json['iduser'],
        'idlocation':request.json['idlocation'],
        'idincidenttype': request.json['idincidenttype'],
        'setimages': request.json['setimages']
    }).inserted_id
    return jsonify(str(id))

@app.route('/incidents', methods=['GET'])
def getIncidents():
    incidents =[]
    for doc in incident_collection.find():
        incidents.append({
            '_id': str(ObjectId(doc['_id'])),
            'idreservation':doc['idreservation'],
            'iduser':doc['iduser'],
            'idlocation':doc['idlocation'],
            'idincidenttype':doc['idincidenttype'],
            'setimages':doc['setimages']
        })
    return (incidents)

@app.route('/incident/<id>', methods=['GET'])
def getIncident(id):
    incident = incident_collection.find_one({'_id':ObjectId(id)})
    print(incident)
    return jsonify({
        '_id': str(ObjectId(incident['_id'])),
        'idreservation':incident['idreservation'],
        'iduser':incident['iduser'],
        'idlocation':incident['idlocation'],
        'idincidenttype':incident['idincidenttype'],
        'setimages':incident['setimages']
    })

@app.route('/incident/<id>', methods=['DELETE'])
def deleteIncident(id):
    incident_collection.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg": 'Incident deleted'})

@app.route('/incident/<id>', methods=['PUT'])
def updateIncident(id):
    incident_collection.update_one({'_id':ObjectId(id)}, {'$set':{
        'idreservation':request.json['idreservation'],
        'iduser':request.json['iduser'],
        'idlocation':request.json['idlocation'],
        'idincidenttype': request.json['idincidenttype'],
        'setimages': request.json['setimages']
    }})
    return jsonify({"msg": 'Incident updated'})

if __name__ == "__main__":
    app.run(debug=True)