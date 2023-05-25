from flask import redirect, render_template, url_for
import pymongo

class User():
    def __init__(self, id, name,lastName, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.lasName=lastName
        self.password = password

 
    
    @staticmethod
    def authenticate(email, password):
        # CONNECTION TO DB
        try:
            mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
            db = mongo.carsRent  
            mongo.server_info()
            print("Connected to MongoDB")
        except:
            print("ERROR - Cannot connect to MongoDB")

        user = db.utilisateurs.find_one({"email": email})

        if user is not None:
            passwordUser = user["password"]

            if passwordUser == password:
                # Authentication successful
                return User(
                    id=str(user["_id"]),
                    name=user["name"],
                    lastName=user["lastName"],
                    email=user["email"],
                    password=user["password"]
                )

        return None
