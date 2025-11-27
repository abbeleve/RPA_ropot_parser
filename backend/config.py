# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/prices")
    output_dir: str = os.getenv("OUTPUT_DIR", "./static/output")

settings = Settings()