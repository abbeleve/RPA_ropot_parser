import os
from typing import List, Dict
from sqlalchemy import create_engine, text, bindparam, String
from sqlalchemy.exc import SQLAlchemyError


class PriceServiceError(Exception):
    pass

class PriceService:
    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            pool_pre_ping=True,
            echo=False
        )
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Проверяет наличие таблицы. В реальном проекте лучше использовать Alembic."""
        with self.engine.connect() as conn:
            result = conn.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'products');"
            ))
            if not result.scalar():
                raise PriceServiceError("Таблица 'products' не найдена в базе данных")

    def get_prices_by_codes(self, codes: List[str]) -> List[Dict[str, any]]:
        if not codes:
            return []

        params = {f"code_{i}": code for i, code in enumerate(codes)}
        placeholders = ", ".join(f":code_{i}" for i in range(len(codes)))
        query = f"SELECT code, name, price, unit FROM products WHERE code IN ({placeholders})"

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params)
                rows = result.fetchall()
        except Exception as e:
            raise PriceServiceError(f"Ошибка при запросе к БД: {e}")

        found = [
            {
                "code": row[0],
                "name": row[1],
                "price": float(row[2]),
                "unit": row[3] or "шт"
            }
            for row in rows
        ]

        found_codes = {item["code"] for item in found}
        missing_codes = [code for code in codes if code not in found_codes]

        if missing_codes:
            raise PriceServiceError(f"Не найдены артикулы: {', '.join(missing_codes)}")

        return found