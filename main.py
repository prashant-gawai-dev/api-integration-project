"""
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from fastapi import HTTPException
app = FastAPI()

@app.get("/")
def read_root():
        return {"message":"Step 1"}

@app.get("/items/{item_id}")
def read_item(item_id: int, detail: bool = False):
    return {"item_id": item_id, "detail": detail}

class APIConfig(BaseModel):
        name: str
        endpoint: str
        auth_type: str
        timeout: int=30
        rate_limit : int=100

@app.post("/configs")
def create_config(config: APIConfig):
        return{"received": config}
{
  "name": "weather_api",
  "endpoint": "https://api.open-meteo.com",
  "auth_type": "none",
  "rate_limit": "{$rate_limit}"
}


@app.get("/weather")
def get_weather(lat:float,lon:float):
response = httpx.get(f"https://api.open-meteo-WRONG.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")
return response.json()
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import httpx
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from model import APIConfig as APIConfigModel

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "It's alive"}


@app.get("/items/{item_id}")
def read_item(item_id: int, detail: bool = False):
    return {"item_id": item_id, "detail": detail}


class APIConfig(BaseModel):
    name: str
    endpoint: str
    auth_type: str
    timeout: int = 30
    rate_limit: int = 100


@app.post("/configs")
def create_config(config: APIConfig, db: Session = Depends(get_db)):
    new_things = APIConfigModel(
        name=config.name,
        endpoint=config.endpoint,
        timeout=config.timeout,
        auth_type=config.auth_type,
        rate_limit=config.rate_limit,
    )
    db.add(new_things)
    db.commit()
    db.refresh(new_things)
    return {"received": new_things}


@app.get("/GetconfigAll")
def get_All_config(db: Session = Depends(get_db)):

    all_configs = db.query(APIConfigModel).all()
    return all_configs


@app.get("/getConfig/{config_id}")
def get_one_config(config_id: int, db: Session = Depends(get_db)):
    oneconfig = db.get(APIConfigModel, config_id)
    if oneconfig is None:
        raise HTTPException(status_code=404, detail="config not found")
    return oneconfig


@app.put("/configUpdate/{config_id}")
def update_config(
    Update_config: APIConfig, config_id: int, db: Session = Depends(get_db)
):
    getConfig = db.get(APIConfigModel, config_id)
    if getConfig is None:
        raise HTTPException(status_code=404, detail="config not found")
    getConfig.name = Update_config.name
    getConfig.endpoint = Update_config.endpoint
    getConfig.timeout = Update_config.timeout
    getConfig.auth_type = Update_config.auth_type
    getConfig.rate_limit = Update_config.rate_limit
    db.add(getConfig)
    db.commit()
    db.refresh(getConfig)
    return {"received": getConfig}


@app.delete("/configDelete/{config_id}")
def deleteConfig(config_id: int, db: Session = Depends(get_db)):
    deleteConfig = db.get(APIConfigModel, config_id)
    if deleteConfig is None:
        raise HTTPException(status_code=404, detail="not found")
    try:
        db.delete(deleteConfig)
        db.commit()
        return {
            "detail": f"Config '{deleteConfig.name}' (id={config_id}) deleted successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed:{str(e)}")


@app.get("/weather")
def get_weather(lat: float, lon: float):
    try:

        """
                response = httpx.get(
            f"https://api.open-meteo-WRONG.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true",
            timeout=5.0,
        )
        """
        response = httpx.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true",
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=502, detail="Could not connect to weather service"
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Weather service timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Weather service error: {e}")
