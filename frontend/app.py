import streamlit as st
import requests

BACKEND_URL = "http://backend:8000"

st.set_page_config(page_title="Умник — RPA", layout="centered")
st.title("🤖 Умник — RPA для ценовой спецификации")
st.write("Загрузите упаковочный лист в формате `.xlsx`")

uploaded_file = st.file_uploader("Выберите файл", type=["xlsx"])

if uploaded_file is not None:
    with st.spinner("Обработка файла..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=30)
            if response.status_code == 200:
                st.success("✅ Файл успешно обработан!")
                st.download_button("Скачать", data=response.content, file_name="spec.pdf", mime="application/pdf")
            else:
                error = response.json().get("detail", "Неизвестная ошибка")
                st.error(f"❌ Ошибка: {error}")
        except Exception as e:
            st.error(f"❌ Ошибка подключения к серверу: {e}")