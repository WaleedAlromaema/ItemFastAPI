from pymongo import MongoClient
from bson import ObjectId
from decouple import config
from typing import Callable, List
from Model.Item import Item


class MongoPyCRUD(object):
    """description of class"""
   
    def __init__(self, *args, **kwargs):
         client = MongoClient()
         database = client["Items_DB_fastapi"]
         self.item_collection = database.get_collection('Items')
        
    
    def parse_item_data(self,item) -> dict:
        return {
            "id": str(item["_id"]),
            "itemType": item["itemType"],
            "newURL": item["newURL"]
            #"startdate": item["StartDate"],
            #"enddate": item["EndDate"]
               }
    def insertItem(self,item:dict) -> dict:
        id=self.item_collection.insert_one(item).inserted_id
        if id:
            return item
        return dict()
    def insertManyItems(self,items:List[dict]) -> List[dict]:
         items_ids = self.item_collection.insert_many(items).inserted_ids
         itemsIds=[ {
                    "id": str(items_ids[i])
                   } 
                     for i in range(len(items_ids))
                 ]
         return itemsIds

    def getItemById(self,id: str) -> dict:
         item = self.item_collection.find_one({"_id": ObjectId(id)})
         if item:
            return item

    def getItemByType(self,type: str) -> dict:
        item = self.item_collection.find_one({"itemType":type})
        if item:
            return Item.parse_obj(item).dict()
            #return self.parse_item_data(item)
    
    def getAllItems(self) -> list:
        items = []
        for _item in self.item_collection.find():
            items.append(Item.parse_obj(_item).dict())

        return items

    def updateItem(self,id: str, item: dict):
        _item = self.item_collection.find_one({"_id": ObjectId(id)})
        if _item:
            self.item_collection.update_one({"_id": ObjectId(id)}, {"$set": item})
            return True

    def removeItemById(self,id: str):
        _item = self.item_collection.find_one({"_id": ObjectId(id)})
        if _item:
            self.item_collection.delete_one({"_id": ObjectId(id)})
            return True

    def removeItemByType(self,type: str):
        _item = self.item_collection.find_one({"type":type})
        if _item:
            self.item_collection.delete_one({"type": type})
            return True
