import streamlit as st
import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime, timedelta

# 1. CONFIGURATION & STYLE
st.set_page_config(page_title="GOLD VVIP - MC ANTHONIO", layout="wide")

# 2. RÉCUPÉRATION PRIX (AVEC SÉCURITÉ)
@st.cache_data(ttl=30)
def get_price():
    try:
        gold = yf.Ticker("GC=F")
        return round(gold.history(period="1d")['Close'].iloc[-1], 2)
    except:
        return 2500.0

current_price = get_price()
now_mg = datetime.now(pytz.timezone('Indian/Antananarivo'))

# 3. SIDEBAR (SENTIMENT & CAPITAL)
st.sidebar.title("🔱 SETTINGS VVIP")
st.sidebar.metric("OR EN DIRECT", f"${current_price}")
sentiment = st.sidebar.slider("% Acheteurs (Foule)", 0, 100, 65)
capital = st.sidebar.number_input("Capital ($)", value=1000)
risk = st.sidebar.slider("Risque %", 1.0, 5.0, 1.0)

# 4. LOGIQUE NEWS & VOLATILITÉ
st.title("🔱 TERMINAL GOLD ELITE - MC ANTHONIO")
is_news = (now_mg.minute % 15 == 0) # Simulation détection news

if is_news:
    st.warning("⚠️ MODE VOLATILITÉ NEWS ACTIVÉ (SL ÉLARGI)")
    sl_pips = 30
else:
    st.success("✅ MARCHÉ STABLE (MADAGASCAR TIME)")
    sl_pips = 15

# 5. SYSTÈME DE PROTECTION +20 PIPS
st.subheader("🛡️ Protection des Gains & Alertes")
entry_p = st.number_input("Ton Prix d'Entrée", value=current_price)
gain_pips = round((current_price - entry_p) * 10, 1) if sentiment > 60 else round((entry_p - current_price) * 10, 1)

if gain_pips >= 20.0:
    st.error(f"💰 +{gain_pips} PIPS ATTEINTS ! SÉCURISEZ AU BE")
    st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/button-10.mp3"></audio>', height=0)
else:
    st.info(f"Suivi des gains : {gain_pips} pips")

# 6. ORDER BOOK & SIGNAL VVIP
col1, col2 = st.columns(2)
with col1:
    st.subheader("🔍 Order Book")
    st.write(f"🧲 Liquidité : {current_price - 5 if sentiment > 60 else current_price + 5}")
    st.write(f"📊 Verdict : {'VENTE' if sentiment > 60 else 'ACHAT'}")

with col2:
    st.subheader("📤 Signal VVIP")
    if st.button("GÉNÉRER LE MESSAGE"):
        msg = f"🔱 VVIP BY MC ANTHONIO 🔱\n📍 Entrée : {current_price}\n🛡️ SL : {current_price+1.5}\n🎯 TP : {current_price-4.5}"
        st.code(msg)

# REFRESH AUTO
st.empty()
