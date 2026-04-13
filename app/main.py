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

    if payload.type not in TYPE_MAP:
        raise HTTPException(
            status_code=400,
            detail="Unsupported type (use: car, flight, electricity)"
        )

    search_query = TYPE_MAP[payload.type]
    try:
        activity_id = get_activity_id(search_query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    url = "https://api.climatiq.io/estimate"

    headers = {
        "Authorization": f"Bearer {CLIMATIQ_KEY}",
        "Content-Type": "application/json"
    }

    if payload.type == "electricity":
        climatiq_body = {
            "emission_factor": {
                "activity_id": activity_id,
                "data_version": DATA_VERSION
            },
            "parameters": {
                "energy": payload.amount,
                "energy_unit": "kWh"
            }
        }
        res = requests.post(url, json=climatiq_body, headers=headers)
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail=res.text)
        data = res.json()
        return {
            "type": "electricity",
            "amount_kwh": payload.amount,
            "co2e": data["co2e"],
            "unit": data["co2e_unit"]
        }