#import the necessary packages
from fastapi import FastAPI,HTTPException
from typing import Union
from pydantic import BaseModel,EmailStr
from database import get_database_connection

#creating a FastAPI app
app=FastAPI()



#Pydantic basemodel is a Python library for data parsing and validation
class User(BaseModel):
    name:str
    email:EmailStr

#Insert a data in the database
@app.post("/users")
async def create_user(user:User):
    try:
        connection=get_database_connection()
        cursor = connection.cursor()#temporary memory used for dml operations
        query = "INSERT INTO users (name,email) VALUES (%s,%s)"
        values = (user.name, user.email)
        cursor.execute(query,values)
        connection.commit()
        connection.close()
        return{"message":"User created SUCCESSFULLY"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
        return {"value is not a valid email address: The email address is not valid. It must have exactly one @-sign."}



@app.get('/')
def index():
    return {"name":"First data"}

#Read the Particular Data using get
@app.get("/users")
async def read_users():
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    connection.close()
    return users

class UpdateUser(BaseModel):
    name:str
    new_email:EmailStr

#update the data in the database
@app.put("/users")
async def update_user(user_update:UpdateUser):
    try:
        connection=get_database_connection()
        cursor = connection.cursor()
        query = "UPDATE users set email=%s where  name=%s"
        values = (user_update.new_email, user_update.name)
        cursor.execute(query,values)
        connection.commit()
        connection.close()
        return{"message":"User Updated SUCCESSFULLY"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
        return {"value is not a valid email address: The email address is not valid. It must have exactly one @-sign."}

class DeleteUser(BaseModel):
    name:str


#delete the data in the database
@app.delete("/users")
async def delete_user(user_delete:DeleteUser):
    try:
        connection=get_database_connection()
        cursor = connection.cursor()
        query = "DELETE From users  where  name=%s"
        values = (user_delete.name,)
        cursor.execute(query,values)
        connection.commit()
        connection.close()
        return{"message":"User deleted SUCCESSFULLY"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
        return {"Row Not Deleted"}


class GetUser(BaseModel):
    name:str

#get the particular data using where condition
@app.get("/users")
async def get_user(user_get:GetUser):
    try:
        connection=get_database_connection()
        cursor = connection.cursor()
        query = "select * From users  where  name=%s"
        values = (user_get.name,)
        cursor.execute(query,values)
        connection.commit()
        connection.close()
        return{"message":"User created SUCCESSFULLY"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
        return {"Data Not Found"}
