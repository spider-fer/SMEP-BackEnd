from app import app 
from config import client
from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId
from datetime import datetime

db = client.smep
user_collection = db.users

fecha = datetime.now()
fecha_string = fecha.strftime("%d/%m/%Y")

@app.route('/users', methods=['POST'])
def createUser():
    if user_collection.find_one({"correo": {"$eq": request.json['correo']}}):
        return jsonify({"msg": 'User with that email already exists'})
    else:
        id = user_collection.insert_one({
            'nombre':request.json['nombre'],
            'apellido':request.json['apellido'],
            'fecharegistro':fecha_string,
            'correo': request.json['correo'],
            'contrasena': request.json['contrasena'],
            'essupervisor': False,
            'incidentes':0
        }).inserted_id
        return jsonify(str(id))

@app.route('/users', methods=['GET'])
def getUsers():
    users =[]
    for doc in user_collection.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'nombre':doc['nombre'],
            'apellido':doc['apellido'],
            'fecharegistro':doc['fecharegistro'],
            'correo':doc['correo'],
            'contrasena':doc['contrasena'],
            'essupervisor':doc['essupervisor'],
            'incidentes':doc['incidentes']
        })
    return (users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = user_collection.find_one({'_id':ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'nombre':user['nombre'],
        'apellido':user['apellido'],
        'fecharegistro':user['fecharegistro'],
        'correo':user['correo'],
        'contrasena':user['contrasena'],
        'essupervisor':user['essupervisor'],
        'incidentes':user['incidentes']
    })

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    user_collection.delete_one({'_id':ObjectId(id)})
    return jsonify({"msg": 'User deleted'})

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    user_collection.update_one({'_id':ObjectId(id)}, {'$set':{
        'nombre':request.json['nombre'],
        'apellido':request.json['apellido'],
        'fecharegistro':request.json['fecharegistro'],
        'correo': request.json['correo'],
        'contrasena': request.json['contrasena'],
        'essupervisor': request.json['essupervisor'],
        'incidentes': request.json['incidentes']
    }})
    return jsonify({"msg": 'User updated'})

if __name__ == "__main__":
    app.run(debug=True)