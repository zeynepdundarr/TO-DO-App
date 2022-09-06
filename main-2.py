from fastapi import FastAPI
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
 

app = FastAPI()


class Item(BaseModel):
    name: str 
    description: Union[str, None] = None
    price: float 
    tax: Union[float, None] = None
    test_feature: str


item_arr = {}

@app.put("/append-item/{item_id}")
async def append_item(item: Item, item_id: int):
    item_dict = item.dict()
    item_arr[item_id] = item

    results = {"success"}
    return results

@app.get("/items/")
async def read_items():
    results = {"items": item_arr}
    # if q:
    #     results.update({"q": q})
    return results

@app.get("/items/{item_id}")
async def read_items(item_id: int):
    results = {"item": item_arr[item_id]}
    # if q:
    #     results.update({"q": q})
    return results

@app.get("/")
async def root():
    return {"message": "Hello world!"}