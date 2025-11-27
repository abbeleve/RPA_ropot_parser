# app/api/v1/prices.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from app.services.price_service import PriceService, PriceServiceError
from app.config import settings

router = APIRouter(prefix="/api", tags=["prices"])

class CodeRequest(BaseModel):
    codes: List[str]

# Инициализация сервиса один раз при запуске приложения
price_service = PriceService(settings.database_url)

@router.post("/prices")
def get_prices_endpoint(request: CodeRequest):
    try:
        result = price_service.get_prices_by_codes(request.codes)
        return result
    except PriceServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервиса: {e}")