from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId

db = client.smep
schedule_collection = db.schedules

@app.route('/schedules', methods=['POST'])
def createSchedule():
    id = schedule_collection.insert_one({
        'idlocation':request.json['idlocation'],
        'descripcion':request.json['descripcion']
    }).inserted_id
    return jsonify(str(id))

@app.route('/schedules', methods=['GET'])
def getSchedules():
    schedules =[]
    for doc in schedule_collection.find():
        schedules.append({
            '_id': str(ObjectId(doc['_id'])),
            'idlocation':doc['idlocation'],
            'descripcion':doc['descripcion']
        })
    return (schedules)

@app.route('/schedule/<id>', methods=['GET'])
def getSchedule(id):
    schedule = schedule_collection.find_one({'_id':ObjectId(id)})
    print(schedule)
    return jsonify({
            '_id': str(ObjectId(schedule['_id'])),
            'idlocation':schedule['idlocation'],
            'descripcion':schedule['descripcion']
    })

@app.route('/schedule/<id>', methods=['DELETE'])
def deleteSchedule(id):
    schedule_collection.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg": 'Schedule deleted'})

@app.route('/schedule/<id>', methods=['PUT'])
def updateSchedule(id):
    schedule_collection.update_one({'_id':ObjectId(id)}, {'$set':{
        'idlocation':request.json['idlocation'],
        'descripcion':request.json['descripcion']
    }})
    return jsonify({"msg": 'Schedule updated'})

if __name__ == "__main__":
    app.run(debug=True)