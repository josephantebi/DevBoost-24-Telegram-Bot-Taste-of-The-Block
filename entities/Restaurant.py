import pydantic


# from entities.Dish import Dish

class Dish(pydantic.BaseModel):
    name: str
    description: str
    price: int


class Restaurant(pydantic.BaseModel):
    name: str
    description: str
    category: str
    user_id: int
    menu: list[Dish]


class TasteOfTheBlock(pydantic.BaseModel):
    restaurants: list[Restaurant]


# class Restaurant:
#     def __init__(self, user_id, name, description):
#         self.user_id = user_id
#         self.name = name
#         self.description = description
#         self.dishes = "list(Dish)"
