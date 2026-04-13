# 🌍 Carbon Tracker API

A FastAPI backend that calculates CO₂ emissions for everyday activities (driving, flying, and electricity usage) using the **Climatiq API**.

---

## Tech Stack

- FastAPI
- Python
- Climatiq API
- Pydantic
- Uvicorn

---

## Features

- Car travel emissions (km)
- Flight emissions (km)
- Electricity usage emissions (kWh)
- Automatic Climatiq activity lookup
- Clean JSON response (CO₂e output only)

---

## How it works

1. User sends an activity request
2. API maps type to Climatiq activity
3. API searches emission factor
4. Climatiq returns CO₂ estimate
5. API returns simplified response

---

## API Endpoints

GET /

Health check

Response:

```json 
{
  "message": "Carbon API running"
}
```

---

## POST /estimate

Calculate CO₂ emissions

Request Body

```json
{
  "type": "car",
  "amount": 100
}
```

**This project uses the Climatiq API for emissions data.**

Docs: [Climatiq Documentation](https://docs.climatiq.io/)  
API Reference: [API Reference](https://docs.climatiq.io/api-reference)  
Estimate Endpoint: [Estimate Endpoint](https://docs.climatiq.io/api-reference/estimate)  
Search Endpoint: [Search Endpoint](https://docs.climatiq.io/api-reference/search)

---

## **Setup Instructions**

### 1. Clone repository  

```bash 
git clone git@github.com:elpah/Carbon-Tracker-API.git carbon-tracker-api
cd carbon-tracker-api  
```

### 2. Create virtual environment  

```bash
python3 -m venv .venv  
source .venv/bin/activate   # macOS / Linux  
``` 

### 3. Install dependencies  

```bash 
python3 -m pip install -r requirements.txt  
```

### 4. Set environment variables  

```bash
Create a `.env` file:
CLIMATIQ_API_KEY=your_api_key_here  
``` 
### 5. Run the server  

```bash
uvicorn app.main:api --reload  
``` 

Server runs at:  
http://127.0.0.1:8000  

---

## Example Requests
The `amount` field represents the activity value (distance in km or energy in kWh depending on type)

### Car  
```bash
curl -X POST http://127.0.0.1:8000/estimate \
-H "Content-Type: application/json" \
-d '{"type":"car","amount":100}'

```

### Flight  

```bash
curl -X POST http://127.0.0.1:8000/estimate \
-H "Content-Type: application/json" \
-d '{"type":"flight","amount":100}'

```

### Electricity

```bash
curl -X POST http://127.0.0.1:8000/estimate \
-H "Content-Type: application/json" \
-d '{"type":"electricity","amount":100}'

```

---

## Future Possible Improvements

- Store fetched data in a database before returning it to the user  
- Add a frontend dashboard for visualizing emissions  
- Expand emission tracking (food, transport, home energy, etc.)  
- Cache Climatiq activity IDs for faster performance  
- Replace `amount` with clearer fields like `distance` and `energy`, depending on activity type  
- Allow multiple activities in one request  

