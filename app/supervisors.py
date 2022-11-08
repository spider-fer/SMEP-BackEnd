from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId

db = client.smep
supervisor_collection = db.supervisor
@app.route('/supervisors', methods=['POST'])
def createSupervisor():
    id = supervisor_collection.insert_one({
        'iduser':request.json['iduser'],
        'idlocation':request.json['idlocation'],
        'fecharegistro':request.json['fecharegistro']
    }).inserted_id
    return jsonify(str(id))

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