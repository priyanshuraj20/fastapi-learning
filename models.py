from pydantic import BaseModel

# these model is for pydantic that is for data validation
class Product(BaseModel):
    id:int
    name:str
    description:str
    price : float
    quantity: int

# we dont need to create constructor by youself once pydantic (data validation is used)
#constructor 
    # def __init__ (self,id:int,name:str,description:str,price:float,quantity:int):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity



