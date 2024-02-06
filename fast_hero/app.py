from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_hero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/hello', response_class=HTMLResponse)
async def hello_page():
    html_content = """<html><head><title>Olá Mundo</title></head><body><h1>Olá Mundo</h1></body></html>"""

    return HTMLResponse(content=html_content, status_code=200)


@app.get('/users/', status_code=200, response_model=UserList)
def read_users():
    return {'users': database}


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.put('/users/{id}', response_model=UserPublic)
def update_user(id: int, user: UserSchema):
    if id > len(database) or id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    user_with_id = UserDB(**user.model_dump(), id=id)
    database[id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{id}', response_model=Message)
def delete_user(id: int):
    if id > len(database) or id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    del database[id - 1]

    return {'message': 'User delete!!'}
