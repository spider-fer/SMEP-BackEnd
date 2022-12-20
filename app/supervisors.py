from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId
from datetime import datetime

db = client.smep
supervisor_collection = db.supervisor
user_collection = db.users
location_collection = db.locations

fecha = datetime.now()
fecha_string = fecha.strftime("%d/%m/%Y")

@app.route('/supervisors', methods=['POST'])
def createSupervisor():
    user = request.json['iduser']
    location = request.json['idlocation']
    if supervisor_collection.find_one({"iduser": {"$eq": user}, "idlocation":{"$eq": location}}):
        return jsonify({"msg": 'Supervisor already exists'})
    else:
        if user_collection.find({"_id": {"$eq": user}}):
            if location_collection.find({"_id": {"$eq": location}}):
                id = supervisor_collection.insert_one({
                    'iduser':user,
                    'idlocation':location,
                    'fecharegistro':fecha_string
                }).inserted_id
                location_collection.update_one({'_id':ObjectId(location)}, {'$set':{
                    'idsupervisor':str(id)
                }})
                user_collection.update_one({'_id':ObjectId(user)}, {'$set':{
                    'essupervisor':True
                }})
                return jsonify(str(id))
            else:
                return jsonify({"msg": 'Location does not exist'})
        else:
            return jsonify({"msg": 'User does not exists'})


@app.route('/supervisors', methods=['GET'])
def getSupervisors():
    supervisors =[]
    for doc in supervisor_collection.find():
        supervisors.append({
            '_id': str(ObjectId(doc['_id'])),
            'iduser':doc['iduser'],
            'idlocation':doc['idlocation'],
            'fecharegistro':doc['fecharegistro']
        })
    return (supervisors)

@app.route('/supervisor/<id>', methods=['GET'])
def getSupervisor(id):
    supervisor = supervisor_collection.find_one({'_id':ObjectId(id)})
    print(supervisor)
    return jsonify({
            '_id': str(ObjectId(supervisor['_id'])),
            'iduser':supervisor['iduser'],
            'idlocation':supervisor['idlocation'],
            'fecharegistro':supervisor['fecharegistro']
    })

@app.route('/supervisor/<id>', methods=['DELETE'])
def deleteSupervisor(id):
    supervisor_collection.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg": 'Supervisor deleted'})

@app.route('/supervisor/<id>', methods=['PUT'])
def updateSupervisor(id):
    supervisor_collection.update_one({'_id':ObjectId(id)}, {'$set':{
        'iduser':request.json['iduser'],
        'idlocation':request.json['idlocation'],
        'fecharegistro':request.json['fecharegistro']
    }})
    return jsonify({"msg": 'Supervisor updated'})

if __name__ == "__main__":
    app.run(debug=True)