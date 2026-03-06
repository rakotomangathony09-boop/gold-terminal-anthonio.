import streamlit as st
import yfinance as yf
import pandas as pd
import pytz
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION INTERFACE ---
st.set_page_config(page_title="GOLD VVIP - MC ANTHONIO", layout="wide")

# Style personnalisé pour un look "Trading Pro"
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #gold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FONCTIONS DE DONNÉES ---
@st.cache_data(ttl=20)
def get_gold_data():
    try:
        gold = yf.Ticker("GC=F")
        hist = gold.history(period="1d", interval="1m")
        return round(hist['Close'].iloc[-1], 2)
    except:
        return 2500.0

current_price = get_gold_data()
tz_mg = pytz.timezone('Indian/Antananarivo')
now_mg = datetime.now(tz_mg)

# --- 3. LOGIQUE NEWS & VOLATILITÉ ---
# Simulation calendrier (USD High Impact)
news_list = [
    {"Heure": (now_mg + timedelta(minutes=10)).strftime("%H:%M"), "Event": "USD - NFP", "Impact": "HIGH"},
    {"Heure": (now_mg + timedelta(hours=1)).strftime("%H:%M"), "Event": "USD - PPI", "Impact": "MEDIUM"}
]
is_news_active = any(abs((datetime.strptime(n["Heure"], "%H:%M").replace(year=now_mg.year, month=now_mg.month, day=now_mg.day, tzinfo=tz_mg) - now_mg).total_seconds()) < 900 for n in news_list)

# --- 4. SIDEBAR (SENTIMENT & RISQUE) ---
st.sidebar.title("🔱 MC ANTHONIO SETTINGS")
st.sidebar.metric("GOLD PRICE", f"${current_price}")

sentiment = st.sidebar.slider("% Acheteurs (Foule)", 0, 100, 65)
balance = st.sidebar.number_input("Capital ($)", value=1000)
golden_zone = st.sidebar.number_input("Prix Golden Zone", value=current_price - 1.5)
entry_price_taken = st.sidebar.number_input("Ton Prix d'Entrée Effectif", value=current_price)

# --- 5. CALCULS STRATÉGIQUES ---
bias = "VENTE (SELL) 🔴" if sentiment > 60 else "ACHAT (BUY) 🟢"
sl_distance = 3.0 if is_news_active else 1.5 # 15 ou 30 pips
sl_final = current_price + sl_distance if "VENTE" in bias else current_price - sl_distance

# Suggestion de Lots
risk_val = balance * 0.01
lots = round(risk_val / (sl_distance * 100), 2)

# --- 6. AFFICHAGE DU TERMINAL ---
st.markdown(f"<h1 style='text-align: center; color: gold;'>🔱 MC ANTHONIO GOLD TERMINAL 🔱</h1>", unsafe_allow_html=True)

if is_news_active:
    st.warning("⚠️ ALERTE NEWS : Volatilité élevée détectée. SL élargi automatiquement.")

col1, col2, col3 = st.columns(3)
col1.metric("VERDICT", bias)
col2.metric("LOTS SUGGÉRÉS", f"{lots}")
col3.metric("STOP LOSS", f"{sl_final}")

# --- 7. SYSTÈME DE PROTECTION & ALERTES ---
st.markdown("---")
st.subheader("🛡️ Protection des Gains & Order Book")

# Alerte Golden Zone
if abs(current_price - golden_zone) <= 0.30:
    st.error("🚨 GOLDEN ZONE PROCHE ! Préparez le signal VVIP.")
    st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-07.wav"></audio>', height=0)

# Alerte +20 Pips
gain_pips = round((current_price - entry_price_taken) * 10, 1) if "ACHAT" in bias else round((entry_price_taken - current_price) * 10, 1)
if gain_pips >= 20.0:
    st.success(f"💰 PROFIT +20 PIPS ATTEINT ! SÉCURISEZ AU BE")
    st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/button-10.mp3"></audio>', height=0)

# Order Book (Liquidité)
st.write(f"🧲 Zone de Liquidité Proche (Target) : **{current_price - 8 if 'VENTE' in bias else current_price + 8}**")

# --- 8. GÉNÉRATEUR SIGNAL VVIP ---
st.markdown("---")
st.subheader("📤 Partage Signal VVIP")
vvip_msg = f"""🔱 **VVIP BY MC ANTHONIO** 🔱
━━━━━━━━━━━━━━━━━━━━
Instrument : **GOLD (XAUUSD)**
Direction : **{bias}**
📍 Entrée : {current_price}
🛡️ Stop Loss : {sl_final}
🎯 Take Profit : {current_price - 4.5 if 'VENTE' in bias else current_price + 4.5}
━━━━━━━━━━━━━━━━━━━━
*Sécurisez à +20 pips !*"""

st.text_area("Copier pour le groupe :", value=vvip_msg, height=200)

# Refresh
time.sleep(30)
st.rerun()
