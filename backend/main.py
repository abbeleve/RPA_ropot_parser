# backend/main.py
import os
import uuid
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from backend.config import settings
from backend.parsers.excel_parser import parse_packaging_list
from backend.services.price_service import PriceService, PriceServiceError
from backend.generators.pdf_generator import generate_pdf_specification

app = FastAPI(title="Умник — RPA для ценовой спецификации")
price_service = PriceService(settings.database_url)

@app.post("/upload")
async def upload_multiple_packaging_lists(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(400, "Нет загруженных файлов")

    all_items = []
    temp_paths = []

    try:
        # Парсим каждый файл
        for file in files:
            if not file.filename.lower().endswith('.xlsx'):
                raise HTTPException(400, f"Файл {file.filename} не является .xlsx")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                tmp.write(await file.read())
                temp_path = tmp.name
                temp_paths.append(temp_path)

            items = parse_packaging_list(temp_path)
            if not items:
                raise HTTPException(400, f"Не удалось извлечь данные из {file.filename}")
            all_items.extend(items)

        if not all_items:
            raise HTTPException(400, "Не найдено ни одной позиции")

        # Получаем цены
        codes = list({item["code"] for item in all_items})
        price_data = price_service.get_prices_by_codes(codes)
        code_to_price = {p["code"]: p for p in price_data}

        # Формируем итоговые позиции
        spec_items = []
        for item in all_items:
            p = code_to_price[item["code"]]
            spec_items.append({
                "name": item["name"],
                "quantity": item["quantity"],
                "unit": p["unit"],
                "price": p["price"]
            })

        # Создаём PDF во временной папке (не в /tmp напрямую)
        output_path = tempfile.mktemp(suffix=".pdf")

        # Генерация PDF
        generate_pdf_specification(spec_items, output_path)

        # Возвращаем файл — НЕ удаляем его здесь!
        return FileResponse(
            path=output_path,
            media_type="application/pdf",
            filename="Ценовая_спецификация.pdf"
        )

    except PriceServiceError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка обработки: {e}")
    finally:
        for p in temp_paths:
            if os.path.exists(p):
                os.remove(p)