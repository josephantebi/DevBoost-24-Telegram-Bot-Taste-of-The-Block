import pydantic

from entities.Dish import Dish


class Restaurant(pydantic.BaseModel):
    name: str
    description: str
    category: str
    user_id: int
    menu: list[Dish]

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "menu": [dish.to_dict() for dish in self.menu]
        }

