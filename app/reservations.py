from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId

db = client.smep
reservation_collection = db.reservation
@app.route('/reservations', methods=['POST'])
def createReservation():
    id = reservation_collection.insert_one({
        'iduser':request.json['iduser'],
        'idschedule':request.json['idschedule']
    }).inserted_id
    return jsonify(str(id))

@app.route('/reservations', methods=['GET'])
def getReservations():
    reservations =[]
    for doc in reservation_collection.find():
        reservations.append({
            '_id': str(ObjectId(doc['_id'])),
            'iduser':doc['iduser'],
            'idschedule':doc['idschedule']
        })
    return (reservations)

@app.route('/reservation/<id>', methods=['GET'])
def getReservation(id):
    reservation = reservation_collection.find_one({'_id':ObjectId(id)})
    print(reservation)
    return jsonify({
            '_id': str(ObjectId(reservation['_id'])),
            'iduser':reservation['iduser'],
            'idschedule':reservation['idschedule']
    })

@app.route('/reservation/<id>', methods=['DELETE'])
def deleteReservation(id):
    reservation_collection.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg": 'Reservation deleted'})

@app.route('/reservation/<id>', methods=['PUT'])
def updateReservation(id):
    reservation_collection.update_one({'_id':ObjectId(id)}, {'$set':{
        'iduser':request.json['iduser'],
        'idschedule':request.json['idschedule']
    }})
    return jsonify({"msg": 'Reservation updated'})

if __name__ == "__main__":
    app.run(debug=True)