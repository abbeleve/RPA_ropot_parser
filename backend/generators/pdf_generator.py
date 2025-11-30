# backend/generators/pdf_generator.py
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
from typing import List, Dict

def generate_pdf_specification(
    items: List[Dict],
    output_path: str
):
    """
    Генерирует PDF-спецификацию без заполнения номера приложения и даты.
    """
    total = sum(item["price"] * item["quantity"] for item in items)

    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    template_dir = os.path.abspath(template_dir)  # на всякий случай

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('spec_template.html')

    html_out = template.render(
        items=items,
        total=total,
        appendix_number="",
        contract_number="",
        contract_date_day="",
        contract_date_month="",
        contract_date_year=""
    )

    HTML(string=html_out).write_pdf(output_path)