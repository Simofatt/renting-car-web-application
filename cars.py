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
            db = mongo.carsRent
            mongo.server_info()
            print("Connected to MongoDB")
        except Exception as e:
            print("ERROR - Cannot connect to MongoDB:", str(e))
            return

        cars_collection = db['cars']
        reservations_collection = db['reservations']

        etat_values = ["terminer", "en_attente"]
        car_ids = reservations_collection.distinct("id_car", {"etat": {"$in": etat_values}})

        query = {"_id": {"$in": car_ids}}
        result = cars_collection.find(query)

        car_list = []
        for car in result:
            car_list.append({
                "model": car["model"],
                "brand": car["brand"],
                "matricule": car["matricule"],
                "year": car["year"],
                "price": car["price"],
                "image": car["image"],
                "id_user": car["id_user"]
            })

        return car_list