# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
from backend.parsers.excel_parser import parse_packaging_list
from backend.services.price_service import PriceService, PriceServiceError
from backend.config import settings
from backend.generators.pdf_generator import generate_pdf_specification
from openpyxl import Workbook

app = FastAPI(title="Умник — RPA для ценовой спецификации")

price_service = PriceService(settings.database_url)

os.makedirs(settings.output_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.output_dir), name="static")

@app.post("/upload")
async def upload_packaging_list(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.xlsx'):
        raise HTTPException(400, detail="Поддерживается только .xlsx")

    temp_path = f"/tmp/{uuid.uuid4()}.xlsx"
    try:
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        items = parse_packaging_list(temp_path)
        if not items:
            raise HTTPException(400, "Не удалось извлечь позиции")

        codes = [item["code"] for item in items]
        price_data = price_service.get_prices_by_codes(codes)
        code_to_price = {p["code"]: p for p in price_data}

        spec_items = []
        for item in items:
            p = code_to_price[item["code"]]
            spec_items.append({
                "name": item["name"],
                "quantity": item["quantity"],
                "unit": p["unit"],
                "price": p["price"]
            })

        # Генерация PDF
        output_filename = f"spec_{uuid.uuid4().hex}.pdf"
        output_path = os.path.join(settings.output_dir, output_filename)

        generate_pdf_specification(spec_items, output_path)

        return FileResponse(output_path, media_type="application/pdf", filename="spec.pdf")

    except PriceServiceError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
@app.get("/health")
def health():
    return {"status": "ok"}