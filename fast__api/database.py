from model import Todo
import motor.motor_asyncio as ma
import pymongo as pym
# client = ma.AsyncIOMotorClient('mongodb://localhost:27017')
client = pym.MongoClient("mongodb://localhost:27017/")
mydb = client['TODOS']
database = client.TodoList
collection = database.todo

async def fetch_one_todo(title):
    doc = collection.find_one({"title":title})
    return doc

async def fetch_all_todo():
    todos = []
    cursor = collection.find({})
    for doc in cursor:
        todos.append(Todo(**doc))
    return todos


async def create_todo(todo):
    doc = todo
    result =  collection.insert_one(doc)
    return doc


async def update_todo(title,description):
    collection.update_one({'title':title},{'$set':{
        "description":description
    }})
    doc = collection.find_one({"title":title})
    return doc

async def remove_todo(title):
    collection.delete_one({'title':title})
    return True
