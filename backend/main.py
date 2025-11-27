# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
from backend.parsers.excel_parser import parse_packaging_list
from backend.services.price_service import PriceService, PriceServiceError
from backend.config import settings

app = FastAPI(title="Умник — RPA для ценовой спецификации")

# Подключаем службу цен (уже инициализирована в prices.py или здесь)
price_service = PriceService(settings.database_url)

# Папка для результатов
os.makedirs(settings.output_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.output_dir), name="static")

@app.post("/upload")
async def upload_packaging_list(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.xlsx'):
        raise HTTPException(400, detail="Поддерживается только .xlsx")

    # Сохраняем временный файл
    temp_path = f"/tmp/{uuid.uuid4()}.xlsx"
    try:
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Парсим Excel
        items = parse_packaging_list(temp_path)
        if not items:
            raise HTTPException(400, "Не удалось извлечь позиции из файла")

        # Получаем цены из "1С" (наш мок)
        codes = [item["code"] for item in items]
        price_data = price_service.get_prices_by_codes(codes)

        # Сопоставляем
        code_to_price = {p["code"]: p for p in price_data}
        spec_items = []
        total = 0.0
        for item in items:
            p = code_to_price[item["code"]]
            amount = p["price"] * item["quantity"]
            total += amount
            spec_items.append({
                "code": item["code"],
                "name": item["name"],
                "quantity": item["quantity"],
                "unit": p["unit"],
                "price": p["price"],
                "amount": amount
            })

        # Генерируем Excel-спецификацию
        from openpyxl import Workbook
        output_filename = f"spec_{uuid.uuid4().hex}.xlsx"
        output_path = os.path.join(settings.output_dir, output_filename)

        wb = Workbook()
        ws = wb.active
        ws.title = "Ценовая спецификация"
        ws.append(["№", "Артикул", "Наименование", "Кол-во", "Ед.", "Цена", "Сумма"])
        for i, row in enumerate(spec_items, start=1):
            ws.append([i, row["code"], row["name"], row["quantity"], row["unit"], row["price"], row["amount"]])
        ws.append(["", "", "", "", "", "ИТОГО:", total])

        wb.save(output_path)

        return {
            "status": "success",
            "download_url": f"/static/{output_filename}",
            "filename": output_filename
        }

    except PriceServiceError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка обработки: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
@app.get("/health")
def health():
    return {"status": "ok"}