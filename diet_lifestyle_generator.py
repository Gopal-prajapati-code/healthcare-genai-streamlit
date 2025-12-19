import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="Diet & Lifestyle Planner", layout="wide")
st.title("🥗 AI Diet & Lifestyle Plan Generator")

st.markdown(
    "⚠️ *This tool provides general health guidance only. It is not medical advice.*"
)

age = st.number_input("Age", min_value=10, max_value=100)
weight = st.number_input("Weight (kg)", min_value=20, max_value=200)

condition = st.selectbox(
    "Medical Condition",
    ["None", "Diabetes", "High Blood Pressure", "Obesity"]
)

goal = st.text_input("Health Goal (e.g., weight loss, sugar control)")
lifestyle = st.selectbox(
    "Lifestyle",
    ["Sedentary", "Moderately Active", "Active"]
)

def generate_plan():
    prompt = f"""
You are a certified health assistant AI.

User Details:
Age: {age}
Weight: {weight} kg
Medical Condition: {condition}
Health Goal: {goal}
Lifestyle: {lifestyle}

Generate:
1. Simple daily diet plan (Indian food preferred)
2. Safe exercise routine
3. Daily schedule
4. Precautions

Rules:
- Use simple language
- No extreme diets
- No medical diagnosis
"""

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4
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

if st.button("Generate Plan"):
    with st.spinner("Generating personalized plan..."):
        plan = generate_plan()
    st.subheader("Your Personalized Health Plan")
    st.write(plan)
