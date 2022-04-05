from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import *

app = FastAPI()
origin = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
    # '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins =  origin,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.get('/')
def root():
    return 'home'

@app.get('/api/todo')
async def get_todo():
    res = await fetch_all_todo()
    return res

@app.get('/api/todo{title}',response_model = Todo)
async def get_todo_by_id(title):
    res = await fetch_one_todo(title)
    if res:
        return res
    else:
        raise HTTPException(404,f"There isn't any todo of title {title}")

@app.post('/api/todo',response_model=Todo)
async def post_todo(todo:Todo):
    res = await create_todo(todo.dict())
    if res:
        return res
    else:
        raise HTTPException(400,"Something Unexpected Happened")


@app.put('/api/todo{title}',response_model = Todo)
async def put_todo(title:str,description:str):
    res = update_todo(title,description)
    if res:
        return res
    else:
        raise HTTPException(404,f"OOpse")

@app.delete('/api/todo{title}')
async def del_todo(title):
    await remove_todo(title)
    if res:
        return "Deletion Successful"
    else:
        raise HTTPException(404,f"Error in deleting")
