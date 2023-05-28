from flask import redirect, render_template,session, url_for
import pymongo

class User():
    def __init__(self, id, name,lastName, email, password,role):
        self.id = id
        self.name = name
        self.email = email
        self.lasName=lastName
        self.password = password
        self.role = role

    @staticmethod
    def get(email):
        try:
            mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
            db = mongo.location_voitures
            mongo.server_info()
            print("Connected to MongoDB")
        except Exception as e:
            print("ERROR - Cannot connect to MongoDB:", str(e))
            return None

        user = db.utilisateur.find_one({"email": email})
        if user:
            return User(
                id=str(user["_id"]),
                name=user["nom"],
                lastName=user["prenom"],
                email=user["email"],
                password=user["password"],
                role=user["role"]
            )
        else:
            return None


 
    
    @staticmethod
    def authenticate(email, password):
        # CONNECTION TO DB
        try:
            mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
            db = mongo.location_voitures 
            mongo.server_info()
            print("Connected to MongoDB")
        except:
            print("ERROR - Cannot connect to MongoDB")

        user = db.utilisateur.find_one({"email": email})

        if user is not None:
            passwordUser = user["password"]

            if passwordUser == password:
                session['role'] = user["role"]
                # Authentication successful
                return User(
                    id=str(user["_id"]),
                    name=user["nom"],
                    lastName=user["prenom"],
                    email=user["email"],
                    password=user["password"],
                    role= user["role"]
                )

        return None
