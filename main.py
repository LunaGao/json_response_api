import urllib.parse

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from deta import Deta

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

deta = Deta()
db = deta.Base("api_db")


@app.post(
    "/create_api/{api_type}/{api_name}",
)
async def create_api(api_type: str, api_name: str, request: Request):
    body = urllib.parse.quote(await request.body())
    api = db.put({"api_name": api_name, "api_body": body, "api_type": api_type})
    return api


@app.post(
    "/edit/{api_key}/{api_type}/{api_name}",
)
async def edit_api(api_type: str, api_key: str, api_name: str, request: Request):
    body = urllib.parse.quote(await request.body())
    db.update({"api_name": api_name, "api_body": body, "api_type": api_type}, api_key)


@app.get(
    "/list_api",
)
def list_api():
    return db.fetch()


@app.delete(
    "/delete/{key}"
)
def delete_api(key: str):
    res = db.delete(key)
    return res


@app.get(
    "/call/{key}"
)
def get_call(key: str, response: Response):
    value = db.get(key)
    if value['api_type'] != 'GET':
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return 'METHOD_NOT_ALLOWED'
    return Response(content=urllib.parse.unquote(value['api_body']))


@app.post(
    "/call/{key}"
)
def post_call(key: str, response: Response):
    value = db.get(key)
    if value['api_type'] != 'POST':
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return 'METHOD_NOT_ALLOWED'
    return Response(content=urllib.parse.unquote(value['api_body']))
