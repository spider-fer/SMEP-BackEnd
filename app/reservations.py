from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId

db = client.smep
reservation_collection = db.reservation
location_collection = db.locations
user_collection = db.users

@app.route('/reservations', methods=['POST'])
def createReservation():
    #Variables introducidas
    iduser = request.json['iduser']
    idlocation = request.json['idlocation']
    hora = request.json['hora']
    fecha = request.json['fecha']
    #Verificar que exista el usuario
    if user_collection.find_one({"_id": {"$eq": iduser}}) and location_collection.find_one({"_id": {"$eq": idlocation}}):
        return jsonify({"msg": 'User or location does not exists'})
    #Verificar que el usuario no tenga otra reservacion a la misma hora y dia 
    if reservation_collection.find_one({"iduser": {"$eq": iduser}, "hora":{"$eq": hora}, "fecha":{"$eq": fecha}}):
        return jsonify({"msg": 'Reservation at that time already exists'})
        
    #Nos traemos la info de la locacion 
    location = location_collection.find_one({'_id':ObjectId(idlocation)})
    #Nos traemos la info de los horarios de la locacion
    horarioinfo = location['horariosinfo']

    for x in range(len(horarioinfo)):
        if str(horarioinfo[x]["hora"]) == hora and horarioinfo[x]["cupousuarios"] > horarioinfo[x]["numusuarios"]:
            horarioinfo[x]["numusuarios"] += 1
            id = reservation_collection.insert_one({
                'iduser':request.json['iduser'],
                'idlocation':idlocation,
                'hora': hora,
                'fecha': fecha
                }).inserted_id
            location_collection.update_one({'_id':ObjectId(idlocation)}, {'$set':{
                'horariosinfo':horarioinfo
            }}) 
            return jsonify(str(id))

    return jsonify({"msg": 'Reservation not created'})
   
@app.route('/reservations', methods=['GET'])
def getReservations():
    reservations =[]
    for doc in reservation_collection.find():
        reservations.append({
            '_id': str(ObjectId(doc['_id'])),
            'iduser':doc['iduser'],
            'idlocation':doc['idlocation'],
            'hora':doc['hora'],
            'fecha':doc['fecha'],
        })
    return (reservations)

@app.route('/reservation/<id>', methods=['GET'])
def getReservation(id):
    reservation = reservation_collection.find_one({'_id':ObjectId(id)})
    print(reservation)
    return jsonify({
            '_id': str(ObjectId(reservation['_id'])),
            'iduser':reservation['iduser'],
            'idlocation':reservation['idlocation'],
            'hora':reservation['hora'],
            'fecha':reservation['fecha']
    })

@app.route('/reservation/<id>', methods=['DELETE'])
def deleteReservation(id):
    reservation_collection.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg": 'Reservation deleted'})

@app.route('/reservation/<id>', methods=['PUT'])
def updateReservation(id):
    reservation_collection.update_one({'_id':ObjectId(id)}, {'$set':{
        'iduser':request.json['iduser'],
        'idlocation':request.json['idlocation'],
        'hora':request.json['hora'],
        'fecha':request.json['fecha']
    }})
    return jsonify({"msg": 'Reservation updated'})

if __name__ == "__main__":
    app.run(debug=True)