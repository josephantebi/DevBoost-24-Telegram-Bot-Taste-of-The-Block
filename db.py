from pymongo import MongoClient

from entities.Restaurant import Restaurant


class RestaurantDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.get_database("taste_of_the_block_bot")
        self.restaurants = self.db.get_collection("restaurants")

    def add_restaurant(self, restaurant: dict):
        new_res = {
            'user_id': restaurant.get("user_id"),
            'name': restaurant.get("name"),
            'description': restaurant.get("description"),
            'category': restaurant.get("category"),
            'menu': restaurant.get("menu", [])
        }
        self.restaurants.insert_one(new_res)
        return self.restaurants.find_one({'user_id': restaurant.get("user_id")})

