from flask import redirect, render_template, url_for
import pymongo

class Cars:
    def __init__(self, model, brand, matricule, year, price, image, id_user):
        self.model = model
        self.brand = brand
        self.matricule = matricule
        self.year = year
        self.price = price
        self.image = image
        self.id_user = id_user

    @staticmethod
    def get():
        # CONNECTION TO DB
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

        etat_values = ["accepter"]
        car_ids = reservations_collection.distinct("voiture_id", {"statut": {"$in": etat_values}})

        query = {"_id": {"$in": car_ids}}
        result = cars_collection.find(query)

        car_list = []
        for car in result:
            car_list.append({
                "model": car["modele"],
                "brand": car["marque"],
                "matricule": car["matricule"],
                "year": car["annee"],
                "price": car["prix"],
                "image": car["image"]
                
            })

        return car_list