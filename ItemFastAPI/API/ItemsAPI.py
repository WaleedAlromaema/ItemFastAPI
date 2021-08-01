from fastapi import FastAPI, Body, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from Model.Item import Item
from Repository.MongoPyCRUD  import MongoPyCRUD
from datetime import datetime
from typing import Callable, List
import bson
import re
from celery_app import *
from celery_app.tasks import *
from celery.result import AsyncResult
from fastapi.responses import JSONResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
mongoPyCRUD= MongoPyCRUD()

async def fetch_result(task_id:str):
    # Fetch result for task_id
        task = AsyncResult(task_id)
        if not task:
            return {'task_id': task_id, 'status': "not exist"}

        if not task.ready():
            return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
        result = task.get()
        return result 


class ItemsAPI(object):
    """description of class"""
   
    @app.get("/", tags=["Root"])
    def get_root() -> dict:
        initItems_task.delay()
        return {
                 "message": "Databse Initialized with samples."
               }

   
    @app.get("/item", tags=["item"], response_model=list)
    async def get_items() ->   list:   
        items =get_items_task.delay()  
        return items.get() 

    @app.get("/item/{itemType}", tags=["item"])
    def get_item(itemType: str) -> dict:
        item = get_item_by_type_task.delay(itemType)
        if item.get():
            return item.get()
        return {
                 "error": "Item with itemType {} dosn't exist".format(itemType)
               }

    @app.get("/item/results/{task_id}", tags=["item"])
    async def fetch_result(task_id:str):
    # get result of task_id
        task = AsyncResult(task_id)
        if not task:
            return {'task_id': task_id, 'status': "not exist"}
        if not task.ready():
            return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
        result = task.get()
        return {'task_id': task_id, 'status': result}

    @app.get("/item/id/{id}", tags=["item"])
    def get_item(id: str) -> Item:
        item =get_item_by_id_task.delay(id)
        if item:
            return  item        
        return {
            "error": "Item with _id {} dosn't exist".format(id)
        }

    @app.post("/item",response_model=Item)
    def add_item(item: Item) -> Item:
        new_item =add_item_task.delay(item.dict())
        return new_item
        return {
            "message": "item added successfully."
        }
 
    # we need to do it by converting from Query ,path,Form ,Cookies,Header.... important from form data
    @app.post("/item/{hastochange}", tags=["item"])
    def update_item(hastochange: str, currentURL= Form(...))  -> dict:
        url=str(currentURL)
        typeValue=parse_url_and_get_type_value_task.delay(url)
        result=typeValue.get()
        if result is None or result=="":
            return {
                "error": "no type spesified in URL "+str(url),
                "result = ": str(result)
                   }
        else :
             item =get_item_by_type_task.delay(result)
             if not item.get():
                 return {
                          "error": "item not exist with type spesified  "+ result +"  in URL"
                        }
             else :
                 
                 _item=item.get()
                 _item["newURL"]= url.replace(result, _item["newURL"]+str(100));
                 return _item
        return {"Item with type= ":result+" not exist"}


    @app.put("/item/{id}", tags=["item"])
    def update_item(id: str, item_data: Item)  -> dict:
        if not get_item_by_id_task.delay(id):
            return {
                "error": "item not exist"
            }

        update_item_task.delay(id, item_data.dict())

        return {
            "message": "item updated successfully."
        }
   
    @app.delete("/item/{id}", tags=["item"])
    def delete_item(id: str) -> Item:
        if not get_item_by_id_task.delay(id):
            return {
                "error": "Invalid _id "
            }


        delete_item_task.delay(id)
        return {
            "message": "item deleted successfully."
        }






