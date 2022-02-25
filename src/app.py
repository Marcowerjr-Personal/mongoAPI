from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util 
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/Test'
mongo = PyMongo(app)
#Primera coleccion 
@app.route('/users', methods=['POST'])
def create_user():
    #recibir datos
    username = request.json['username']
    password =request.json['password']
    email = request.json['email']

    if  username and password and email:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {'username': username,
            'email': email,
            'password': hashed_password}
        )
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email
        }
        return response
    else:
        return not_found()

@app.route('/users', methods=['GET'])
def get_user():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_userid(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json') 

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + 'was Deleted successfully'})
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    email = request.json['email']
    password =request.json['password']

    if  username and password and email:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username' : username,
            'password' : hashed_password,
            'email' : email
        }})
        response = jsonify({'message': 'User' + id + 'was update successfully'})
        return response

#Segunda coleccion
@app.route('/teacher', methods=['POST'])
def create_teacher():
    #recibir datos
    name = request.json['name']
    last_name =request.json['last_name']
    age = request.json['age']

    if  name and last_name and age :
        id = mongo.db.teacher.insert_one(
            {'name ': name ,
            'last_name': last_name,
            'age ': age }
        )
        response = {
            'id': str(id),
            'name ': name ,
            'last_name': last_name,
            'age ': age 
        }
        return response
    else:
        return not_found()


@app.route('/teacher', methods=['GET'])
def get_teacher():
    teacher = mongo.db.teacher.find()
    response = json_util.dumps(teacher)
    return Response(response, mimetype='application/json')

@app.route('/teacher/<id>', methods=['GET'])
def get_teacherid(id):
    teacher = mongo.db.teacher.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(teacher)
    return Response(response, mimetype='application/json') 

@app.route('/teacher/<id>', methods=['DELETE'])
def delete_teacher(id):
    mongo.db.teacher.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Teacher' + id + 'was Deleted successfully'})
    return response

@app.route('/teacher/<id>', methods=['PUT'])
def update_teacher(id):
    name = request.json['name']
    last_name = request.json['last_name']
    age  =request.json['age ']

    if  name and last_name and age:
        mongo.db.teacher.update_one({'_id': ObjectId(id)}, {'$set': {
            'name' : name ,
            'last_name' : last_name,
            'age' : age
        }})
        response = jsonify({'message': 'Teacher' + id + 'was update successfully'})
        return response

#Tercera collection
@app.route('/videogame', methods=['POST'])
def create_videogame():
    #recibir datos
    name_videogame = request.json['name_videogame']
    genre =request.json['genre']

    if  name_videogame and genre:
        id = mongo.db.videogame.insert_one(
            {'name_videogame': name_videogame ,
            'genre': genre }
        )
        response = {
            'id': str(id),
            'name_videogame': name_videogame ,
            'genre': genre
        }
        return response
    else:
        return not_found()

@app.route('/videogame', methods=['GET'])
def get_videogame():
    videogame = mongo.db.videogame.find()
    response = json_util.dumps(videogame)
    return Response(response, mimetype='application/json')

@app.route('/videogame/<id>', methods=['GET'])
def get_videogameid(id):
    videogame = mongo.db.videogame.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(videogame)
    return Response(response, mimetype='application/json') 

@app.route('/videogame/<id>', methods=['DELETE'])
def delete_videogame(id):
    mongo.db.videogame.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Videogame' + id + 'was Deleted successfully'})
    return response

@app.route('/videogame/<id>', methods=['PUT'])
def update_videogame(id):
    videogame  = request.json['videogame']
    genre  = request.json['genre ']

    if  videogame and genre:
        mongo.db.videogame.update_one({'_id': ObjectId(id)}, {'$set': {
            'videogame ' : videogame ,
            'password' : genre
        }})
        response = jsonify({'message': 'Videogame' + id + 'was update successfully'})
        return response

# Para recivir error y enviar avisos
@app.errorhandler(400)
def not_found(error=None):
    response = jsonify({
        'message': 'Resoure Not Found' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)