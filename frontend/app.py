# frontend/app.py
import streamlit as st
import requests
from io import BytesIO

# BACKEND_URL = "http://localhost:8000"  # если Streamlit локально
BACKEND_URL = "http://backend:8000"      # если Streamlit в Docker

st.set_page_config(page_title="Умник — RPA", layout="centered")
st.title("🤖 Умник — RPA для ценовой спецификации")
st.write("Загрузите **несколько** упаковочных листов в формате `.xlsx`")

# Множественная загрузка
uploaded_files = st.file_uploader(
    "Выберите файлы",
    type=["xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Выбрано файлов: {len(uploaded_files)}")
    file_details = []
    for f in uploaded_files:
        file_details.append((f.name, f.getvalue()))
    
    if st.button("✅ Обработать все файлы"):
        with st.spinner("Обработка..."):
            files = [
                ("files", (name, content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
                for name, content in file_details
            ]
            try:
                response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=60)
                if response.status_code == 200 and response.headers.get('content-type') == 'application/pdf':
                    st.download_button(
                        label="⬇️ Скачать объединённую спецификацию",
                        data=response.content,
                        file_name="Ценовая_спецификация.pdf",
                        mime="application/pdf"
                    )
                else:
                    try:
                        err = response.json().get("detail", "Неизвестная ошибка")
                    except:
                        err = response.text[:200] or "Сервер вернул пустой ответ"
                    st.error(f"Ошибка: {err}")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")
else:
    st.warning("Загрузите хотя бы один файл.")