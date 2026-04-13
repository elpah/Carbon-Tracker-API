from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests
import os

load_dotenv()

api = FastAPI()

CLIMATIQ_KEY = os.getenv("CLIMATIQ_API_KEY")


@api.get("/")
def index():
    return {"message": "endpoint reached"}


@api.post("/estimate")
def get_estimate(data: dict):

    url = "https://api.climatiq.io/estimate"

    headers = {
        "Authorization": f"Bearer {CLIMATIQ_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=response.text)

    return response.json()