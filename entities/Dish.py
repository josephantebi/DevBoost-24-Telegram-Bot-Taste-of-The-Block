import pydantic


class Dish(pydantic.BaseModel):
    name: str
    description: str
    price: int

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price
        }