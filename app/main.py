from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os

load_dotenv()

api = FastAPI()

CLIMATIQ_KEY = os.getenv("CLIMATIQ_API_KEY")
DATA_VERSION = "32.32"


class EstimateRequest(BaseModel):
    type: str
    amount: float

TYPE_MAP = {
    "car": "passenger vehicle car petrol",
    "flight": "flight passenger",
    "electricity": "electricity grid"
}


def get_activity_id(query: str):
    url = "https://api.climatiq.io/search"

    headers = {
        "Authorization": f"Bearer {CLIMATIQ_KEY}"
    }
    params = {
        "query": query,
        "data_version": DATA_VERSION
    }
    res = requests.get(url, headers=headers, params=params)

    if res.status_code != 200:
        raise Exception(res.text)
    data = res.json()
    if not data.get("results"):
        raise Exception("No activity found")
    return data["results"][0]["activity_id"]

@api.get("/")
def index():
    return {"message": "Carbon API running"}

@api.post("/estimate")
def estimate(payload: EstimateRequest):
    return {"status": "ok"}
