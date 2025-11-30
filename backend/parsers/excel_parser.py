# app/parsers/excel_parser.py
import pandas as pd
from typing import List, Dict, Any

def parse_packaging_list(file_path: str) -> List[Dict[str, Any]]:
    """
    Парсит Excel-файл с упаковочным листом.
    Предполагается, что:
      - заголовки в строке 5 (A5...),
      - артикул в формате строки с ведущими нулями (например, '0000001')
    """
    try:
        df = pd.read_excel(
            file_path,
            header=4, 
            dtype={'Артикул': str} 
        )
    except Exception as e:
        raise ValueError(f"Не удалось прочитать Excel: {e}")

    if 'Артикул' not in df.columns or 'Наименование' not in df.columns or 'Количество' not in df.columns:
        raise ValueError("В файле отсутствуют обязательные колонки: Артикул, Наименование, Количество")

    items = []
    for _, row in df.iterrows():
        code = row['Артикул']
        name = row['Наименование']
        qty_raw = row['Количество']

        if pd.isna(code) and pd.isna(name):
            continue

        if pd.isna(code) or str(code).strip().lower() == 'nan':
            continue
        code = str(code).strip()

        if pd.isna(name) or str(name).strip().lower() == 'nan':
            continue
        name = str(name).strip()

        try:
            qty = float(str(qty_raw).replace(',', '.'))
        except (ValueError, TypeError):
            continue

        items.append({
            "code": code,
            "name": name,
            "quantity": qty
        })

    if not items:
        raise ValueError("Не найдено ни одной валидной позиции")

    return items