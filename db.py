from pymongo import MongoClient


class ShoppingDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.get_database("shopping_bot")
        self.lists = self.db.get_collection("lists")
        self.lists.create_index("chat_id", unique=True)

    def add_item(self, chat_id: int, item: str):
        self.lists.update_one({'chat_id': chat_id}, {
            '$push': {"items": item}
        }, upsert=True)
        return self.lists.find_one({'chat_id': chat_id})['items']


