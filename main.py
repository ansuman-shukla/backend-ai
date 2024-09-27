from typing import Union

from fastapi import FastAPI
from services.ai import process_request


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/start")
def get_response(youtube_url: str):
    print("The request is processing now!")
    history = [

    ]
    response = process_request(youtube_url, history)
    print(type(response))
    # convert the response to json
    response = response.text
    return response
