import urllib.parse

from fastapi import FastAPI, Request, Response
from deta import Deta

app = FastAPI()
deta = Deta()
db = deta.Base("api_db")


@app.post(
    "/create_api/{api_type}/{api_name}",
)
async def create_api(api_type: str, api_name: str, request: Request):
    body = urllib.parse.quote(await request.body())
    api = db.put({"api_name": api_name, "api_body": body, "api_type": api_type})
    return api


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
def get_call(key: str):
    return Response(content=urllib.parse.unquote(db.get(key)['api_body']))


@app.post(
    "/call/{key}"
)
def post_call(key: str):
    return Response(content=urllib.parse.unquote(db.get(key)['api_body']))
