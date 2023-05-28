from flask import redirect, render_template, url_for
import pymongo
class Cars:
    def __init__(self, model, brand, matricule, year, price, image, id_user, id,statut):
        self.model = model
        self.brand = brand
        self.matricule = matricule
        self.year = year
        self.price = price
        self.image = image
        self.id_user = id_user
        self.id = id
        self.statut = statut


    @staticmethod
    def get():
        try:
            mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
            db = mongo.location_voitures
            mongo.server_info()
            print("Connected to MongoDB")
        except Exception as e:
            print("ERROR - Cannot connect to MongoDB:", str(e))
            return

        cars_collection = db['voiture']
        reservations_collection = db['reservation']

        result = cars_collection.find()

        car_list = []
        for car in result:
            reservation = reservations_collection.find_one({"voiture_id": car["_id"]})
            statut = reservation["statut"] if reservation else None

            car_list.append({
                "_id": car["_id"],
                "model": car["modele"],
                "brand": car["marque"],
                "matricule": car["matricule"],
                "year": car["annee"],
                "price": car["prix"],
                "image": car["image"],
                "statut": statut
            })

        return car_list
