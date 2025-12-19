import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="Medical Report Summarizer", layout="wide")
st.title("🏥 Medical Report Summarization (Generative AI)")

st.markdown(
    "⚠️ *This tool is for educational purposes only and does not provide medical advice.*"
)

report_text = st.text_area(
    "Paste Medical Report (Dummy / Sample Data Only)",
    height=250
)

def summarize_report(report):
    prompt = f"""
You are a medical assistant AI.

Task:
- Convert the medical report into simple, patient-friendly language
- Avoid medical jargon
- Explain conditions briefly
- Do NOT provide diagnosis or emergency advice

Medical Report:
{report}

Output:
Patient-friendly summary:
"""

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return response.json()["choices"][0]["message"]["content"]

if st.button("Generate Summary"):
    if report_text.strip():
        with st.spinner("Summarizing report..."):
            summary = summarize_report(report_text)
        st.subheader("Patient-Friendly Summary")
        st.write(summary)
    else:
        st.warning("Please paste a medical report.")
