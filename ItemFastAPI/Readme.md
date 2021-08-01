# Items FastAPI + Celery with result backend 
-----------
Author : Waleed Alromaema
         wal.roma@outlook.it
-----------
###Content:

1- About The API.

2- Item Database Design

	   a- Database Design
	   b- Business Logic Design
	   c- Rest API Interface
   
3- Runing Application

----------------
## 1- About Items API.

Item API is Microservice REST API Application developed by FastAPI. It provide the following Services:

- Get :
     - All Items in Mongo DB
- Post :
     - Send Parameter of URL 
     - Post Function Parse URL and Get Type.
     - then It Quary Database for Item by Type.
     - Return the result. 
- Get:
    - get item by type
    - get all items
    - get item by id
- Put:
    - update item
- Delete:
    - delete item by id.
  

## 2- Item Database Design

### A- Database Design

the Database consists of only one Collection Items.
   
### B- Business Logic Design

The design pattern considered the separation between different layers,  
- Presentation layer [her is the Cellery workers Tasks Provider] 
     - using cellery worker tasks to serve api needs.
     
- Business Logic Layer
     - using domain objects in Model as Item Class that inhrits from BaseModel pyndantics support.
     
- Repository Data Access Layer 
     - It implements MongoCRUD for all needed DB operation on Item
 
       
### C-Rest API Interface
 
 below are the set of REST Services and the associated URI.
 
 ![alt ItemEndpoints](ItemEndpoints.PNG)   

## 3- Setting and Running Application
	    
### The tools required are: 
-  visual Studio 2019
-  Docker and Docker compose installed for windows
-  POSTMAN Chrome application for client test of rest service in server side download from https://go.pstmn.io/ 


#### - Git Link

```
https://github.com/WaleedAlromaema/ItemFastAPI.git
```

#### - POSTMAN

using postman for testing the Rest api service
Enter in URL: LOCALHOST:PORT/../...
as in the rest api listed above:

###here is an example of GET Item result:

![alt getItem](ItemsGet.PNG)

### Example of Item Post :

![alt postItem](ItemsPost.PNG)


### Run example step by step:
1. Run App  with docker-compose in case of docker use:
```sh
docker-compose up -d
```

2. Run application:
```sh
uvicorn API.ItemsAPI:app --reload
```

3. Run celery worker:
```sh
celery -A celery_app.celery_app worker --pool=solo -l info -Q items-queue -c 1 -E
```

4. Open API doc: [http://127.0.0.1:8000](http://127.0.0.1:8000)
5. Open Flower: [http://127.0.0.1:5555/flower](http://127.0.0.1:5555/flower)
