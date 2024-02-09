from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_hero.routes import auth, user
from fast_hero.schemas import Message, Token

app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)


@app.post('/token', response_model=Token)
@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/hello', response_class=HTMLResponse)
async def hello_page():
    html_content = """<html><head><title>Olá Mundo</title></head><body><h1>Olá Mundo</h1></body></html>"""

    return HTMLResponse(content=html_content, status_code=200)
