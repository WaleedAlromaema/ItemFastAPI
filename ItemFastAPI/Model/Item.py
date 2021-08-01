from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class Item(BaseModel):
    itemType:str
    newURL:str 
    startDate:Optional[datetime]
    endDate:Optional[datetime]

  
   




