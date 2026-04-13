from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
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

@api.get("/")
def index():
    return {"message": "Carbon API running"}

