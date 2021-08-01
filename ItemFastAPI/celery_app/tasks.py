from time import sleep
from celery import current_task
from celery_app import celery_app

from fastapi.encoders import jsonable_encoder
from Model.Item import Item
from Repository.MongoPyCRUD  import MongoPyCRUD
from datetime import datetime
from typing import Callable, List
import bson
import re
from celery.utils.log import get_task_logger
 

logger=get_task_logger(__name__)

mongoPyCRUD=MongoPyCRUD()

@celery_app.task(acks_late=True, queue="items-queue")
def parse_url_and_get_type_value_task(url):
        logger.info(f"Url to search is : {url}")
        #pattern = r"&type=(\S*)"
        pattern = r"&type=([^&]*)"
        pattern_compiled = re.compile(pattern, flags=re.IGNORECASE)
        match = pattern_compiled.search(url)
        if match is None:
            return None

        logger.info(f"The result match is , {match.group(1)} ")
       
        typeValue=match.group(1)
        
        return typeValue

@celery_app.task(acks_late=True, queue="items-queue")
def initItems_task():
     ls=[]
     for i in range(10):
         item=bson.SON()
         item["itemType"]="Iphone"+str(i)
         item["newURL"]="URL"+str(i)
         item["startDate"]=datetime.now()
         item["endDate"]=datetime(2022,12,29,12,30,30)
         ls.append(item)   
     mongoPyCRUD.insertManyItems(ls)

@celery_app.task(acks_late=True, queue="items-queue")
def get_items_task() :   
        items = mongoPyCRUD.getAllItems()  
        counts=len(items)
        logger.info(f"Items returned {counts}")
        #current_task.update_state(state='Finished',
        #                           meta={'process_percent': 100})
        return items

@celery_app.task(acks_late=True, queue="items-queue")
def get_item_by_type_task(itemType: str) -> dict:
        item = mongoPyCRUD.getItemByType(itemType)
        
        return item
        
@celery_app.task(acks_late=True, queue="items-queue")
def get_item_by_id_task(id: str) -> Item:
        item =mongoPyCRUD.getItemById(id)
        current_task.update_state(state='Finished',
                                  meta={'process_percent': 100})
        return  item
    
@celery_app.task(acks_late=True, queue="items-queue")
def add_item_task(item: Item) -> Item:
        new_item = mongoPyCRUD.insertItem(item.dict())
        current_task.update_state(state='Finished',
                                  meta={'process_percent': 100})
        return new_item
@celery_app.task(acks_late=True, queue="items-queue")
def update_item_task(id: str, item_data: Item) :
        mongoPyCRUD.updateItem(id, item_data.dict())
        current_task.update_state(state='Finished',
                                  meta={'process_percent': 100})
        
       
@celery_app.task(acks_late=True, queue="items-queue")
def delete_item_task(id: str) -> Item:
        mongoPyCRUD.removeItemById(id)
        current_task.update_state(state='Finished',
                                  meta={'process_percent': 100})
        
        
