 ## FastAPI Notes
this is a brief short notes taken from fastapi documentation
### Def:
- fastapi is a python based web API 

### Installation

```
 pip install fastapi pydantic uvicorn
```
   - uvicorn is an instance of server AGIS 
### Usage:
```
 from fastapi import FastAPI
 from fastapi.middleware.cors import CORSMiddleware

 app = FastAPI()
 app.add_middleware(
	 	                 CORSMiddleware,
		                 allow_origins=['*'],
		                 allow_credentials=True,
		                 allow_methods=['*'],
		                 allow_headers=['*'],
	                   )

 @app.get("/{...}")   
 @app.post("/{...}")   
 @app.put("/{...}")   
 @app.delete("/{...}")
     method()

```
##### - Method Signiture and Parameters:

```
async def method_name( parameters) -> returnType:
     
          return var
```
parameters can be taken from **Path,Query,Body,Form,Header,Cookies,...**
#### A- param from path url must have the following formate:
	      1- simple value var
             @app.get( "url:/path/{var}")
		  2- file path 
		     @app.get( "url:/files/{file_path:path}")
		     in url you can write : "url:"/path//path" with // 
		  3- mult path param
		     @app.get("/users/{user_id}/items/{item_id}")
		  4- pass string of enum type
		     @app.get("/models/{model_name}")
              async def get_model(model_name: ModelName):

			   ModelName is an enum class
			   class ModelName(str, Enum):
						alexnet = "alexnet"
						resnet = "resnet"
						lenet = "lenet"
		  
		 
#### B- param from Query:
The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.
          
For example:

 in the URL: http://127.0.0.1:8000/items/?skip=0&limit=10
.         the query parameters are:
skip: with a value of 0
limit: with a value of 10
###### Parameters types:
    1- param with default values if not spesified
		   @app.get("/items/")
           async def read_item(skip: int = 0, limit: int = 10):
	2- param with path and optional params :
    	   @app.get("/items/{item_id}")
           async def read_item(item_id: str, q: Optional[str] = None):
    3- params with intial optional 
		   @app.get("/items/{item_id}")
           async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
	4- Query param validation and initalization 
		  @app.get("/items/")
              async def read_items( q: Optional[str] = Query(
			                                                    ###### for string ...
																None,
																alias="item-query",  ###if item-query is not valid param name and we wnt it to be use alias
																title="Query string",
																description="Query string for the items to search in the database that have a good match",
																min_length=3,
																max_length=50,
																regex="^fixedquery$",
																deprecated=True,
																
																###### for numbers 
																gt=0,    # >
																lt=10.5  # <=
											                 )
                                   ):
		 
	5- if param of type list it declared in url as : http://localhost:8000/items/?q=foo&q=bar
		        @app.get("/items/")
   			      async def read_items( q: list) or
				  async def read_items( q: List[str])


#### C- param from Body:
the sam as Query params but it must be of Json or dict or any Pydantic subtype:
		 notes:
		 
	1- param item: Item from Body
		   @app.put("/items/{item_id}")
             async def create_item(item_id: int, item: Item, q: Optional[str] = None):
               result = {"item_id": item_id, **item.dict()}
		 
	2- embed=True means Json object Item can be an attribue of the body with attripute name "item":{} , with in Json body.
		   @app.put("/items/{item_id}")
            async def update_item(item_id: int, item: Item = Body(..., embed=True))
			
	3- Body Field same as others but applyed to class models 
	 
	 example:
				from typing import Optional
				from fastapi import Body, FastAPI
				from pydantic import BaseModel, Field

				app = FastAPI()
				
				class Item(BaseModel):
					name: str
					description: Optional[str] = Field(
														None, title="The description of the item", max_length=300
													  )
					price: float = Field(..., gt=0, description="The price must be greater than zero")
					tax: Optional[float] = None

				@app.put("/items/{item_id}")
    				async def update_item(item_id: int, item: Item = Body(..., embed=True)):
	    				results = {"item_id": item_id, "item": item}
		    			return results

#### D- Respone Model:
    - @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"}, response_model_exclude_unset=True)
		  
  also we can use 

     - `response_model_exclude_defaults=True`
     - `response_model_exclude_none=True`
#### E- param as File
- form data enctype="multipart/form-data"
- file recived as Byte uploaded in memory. # good for small files
- file recived as UploadFile has more benifit of on disk stor it has the following async methods:

      - write(data): Writes data (str or bytes) to the file.
	  - read(size): Reads size (int) bytes/characters of the file.
	  - seek(offset): Goes to the byte position offset (int) in the file.
					    E.g., await myfile.seek(0) would go to the start of the file.
					    This is especially useful if you run await myfile.read() once and then need to read the contents again.
	  - close(): Closes the file.
			    As all these methods are async methods, you need to "await" them.
			    For example, inside of an async path operation function you can get the contents with:
			          - contents = await myfile.read()
				 If you are inside of a normal def path operation function, you can access the UploadFile.file directly, for example:
                        - contents = myfile.file.read()				  
	        example:
				from typing import List
				from fastapi import FastAPI, File, UploadFile
				from fastapi.responses import HTMLResponse

				app = FastAPI()

				@app.post("/files/")
				async def create_files(files: List[bytes] = File(...)):
					return {"file_sizes": [len(file) for file in files]}


				@app.post("/uploadfiles/")
				async def create_upload_files(files: List[UploadFile] = File(...)):
					return {"filenames": [file.filename for file in files]}


				@app.get("/")
				async def main():
					content = """
				<body>
				<form action="/files/" enctype="multipart/form-data" method="post">
				<input name="files" type="file" multiple>
				<input type="submit">
				</form>
				<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
				<input name="files" type="file" multiple>
				<input type="submit">
				</form>
				</body>
					"""
					return HTMLResponse(content=content)
#### F- Statuse code to return:
	      - @app.post("/items/", status_code=201)
          example:
```
from fastapi import FastAPI, status
	app = FastAPI()
	@app.post("/items/", status_code=status.HTTP_201_CREATED)
	async def create_item(name: str):
		return {"name": name}

```	  
In short:

- 100 and above are for "Information". You rarely use them directly. Responses with these status codes cannot have a body.
- 200 and above are for "Successful" responses. These are the ones you would use the most.
				  200 is the default status code, which means everything was "OK".
				  Another example would be 201, "Created". It is commonly used after creating a new record in the database.
				  A special case is 204, "No Content". This response is used when there is no content to return to the client, and so the response must not have a body.
- 300 and above are for "Redirection". Responses with these status codes may or may not have a body, except for 304, "Not Modified", which must not have one.
- 400 and above are for "Client error" responses. These are the second type you would probably use the most.
				  An example is 404, for a "Not Found" response.
				  For generic errors from the client, you can just use 400.
- 500 and above are for server errors. You almost never use them directly. When something goes wrong at some part in your application code, or server, it will automatically return one of these status codes.


### Add routers
```
app=FastAPI()
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
```

Admin module
```
from fastapi import APIRouter
router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}	
```	
Or details in router prefered :
```
pp=FastAPI()
app.include_router( admin.router)
-------Admin module
from fastapi import APIRouter

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
	)


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}	
```
dependencies=[Depends(get_token_header)]  : her get_token_header is a method imported from other module

### Run Fatsapi App:
-  Run by server 
   - Command :
      -  uvicorn API.ItemsAPI:app --reload
- Run by python file compile 
   - main.py 
```
import uvicorn
if __name__ == '__main__':
		uvicorn.run("API.ItemsAPI:app", host="127.0.0.1", port=8000, reload=True)
```
then in shell:
```
run $ python main.py
```

recommended to use host  host="0.0.0.0" in Docker