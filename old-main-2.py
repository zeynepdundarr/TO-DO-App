from click import password_option, style
from fastapi import FastAPI
app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the curr user"}

# from enum import Enum

# from pydantic import BaseModel

# class ModelTypes(str, Enum):
#     abc = "abcmodel"
#     bcd = "bcdmodel"
#     deg = "degmodel"

# @app.get("/models/{model_name}")
# async def get_model_name(model_name: ModelTypes):
#     if model_name is ModelTypes.abc:
#         return {"model_name": model_name, "message" : "Deep Learning FTW!"}
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "Have some residuals"}
#     return {"model_name: ": model_name, "message": "else case"}

fake_items = [{"item1": 1},{"item2": 2},{"item3": 3}]

# @app.get("/items/")
# async def read_items(skip: int = 0, limit: int = 10):
#     return fake_items[skip: skip+limit]

# @app.get("/items/{item_id}")
# async def read_items(item_id:str, item_name):
#     items = {"item_id": item_id, "item_name": item_name}
#     return items

# from typing import Union
# from fastapi import FastAPI
# from pydantic import BaseModel

# class User(BaseModel):
#     name: str 
#     surname: str 
#     password: str = None
#     mail: str = None

# @app.post("/items/")
# async def create_item(user: User):
#     return user

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str 
    description: Union[str, None] = None
    price: float 
    tax: Union[float, None] = None
    test_feature: str

app = FastAPI()

# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict
    
item_arr = {}

@app.post("/append-item/{item_id}")
async def create_item(item: Item, item_id: int):
    item_dict = item.dict()
    item_arr[item_id] = item
    return item_arr

@app.get("/items/")
async def read_items(q: Union[str, None] = None):
    results = {"items": item_arr}
    # if q:
    #     results.update({"q": q})
    return results

# @app.get("/items/")
# async def read_items(q: Union[str, None] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


class Family:
    id : int
    mom: str
    dad: str
    years_married: int = 22
    current_year: int = 2022
    wedding_date: int


@app.post("/family_info/")
async def post_fam(family: Family):
    family_dict = family.dict()
    if family.current_year:
        wedding_date = family.current_year - family.years_married
        family_dict.update({"wedding_date":wedding_date, "mom": "Dilek"})
    return family_dict

@app.get("/family_info/")
async def read_family():


